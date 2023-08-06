import time
from typing import Optional, Tuple

import botocore
from botocore.exceptions import ClientError

# todo: fix issue where when deploying we do not check if the api with the id found in the settings file do exit
from inoft_vocal_engine.cloud_providers.aws.aws_core import AwsCore
from inoft_vocal_engine.cloud_providers.aws.generated_code_s3_client import GeneratedCodeS3Client
from inoft_vocal_engine.cloud_ressources.account_resources import AccountResources
from inoft_vocal_engine.cloud_ressources.engine_resources import EngineResources
from inoft_vocal_engine.cloud_ressources.project_resources import ProjectResources
from inoft_vocal_engine.databases.dynamodb.accounts_data_dynamodb_client import AWSBuildInfosBackendModel
from inoft_vocal_engine.utils.paths import get_inoft_vocal_engine_root_path
from inoft_vocal_framework.utils.general import generate_uuid4


class DeployHandler(AwsCore):
    def __init__(self):
        print("Initializing AWS clients... (this can take a few seconds)")
        start_time = time.time()
        super().__init__(clients_to_load=[AwsCore.CLIENT_S3, AwsCore.CLIENT_LAMBDA, AwsCore.CLIENT_API_GATEWAY,
                                          AwsCore.CLIENT_IAM, AwsCore.CLIENT_STS, AwsCore.CLIENT_BOTO_SESSION])
        print(f"Took {round(time.time() - start_time, 2)}s to initiate AWS clients")
        # todo: make the initialization even more asynchronous, by calling the handle function while the AWS ressources are initializing.
        #  Right now, the initialization of the resources are async, but we must wait for their completion in order to call the handle function.

    def deploy_deprecated(self, lambda_files_root_folderpath: str, stage_name: str, bucket_name: str, bucket_region_name: str,
               lambda_name: str, lambda_handler: str, runtime="python3.7", upload_zip: bool = True,
               existing_zip_filepath: Optional[str] = None, lambda_description: str = "Inoft Vocal Engine Deployment",
               lambda_timeout_seconds: int = 30, lambda_memory_size: int = 512, publish: bool = True):
        pass

    def _try_to_update_lambda_code(self, lambda_arn: str, bucket_name: str, object_key_name: str, handler_function_path: str) -> bool:
        try:
            self.update_lambda_function_code(lambda_arn=lambda_arn, object_key_name=object_key_name, bucket_name=bucket_name)
            self.update_lambda_function_configuration(function_name=lambda_arn, handler_function_path=handler_function_path)
            print(f"Updated the code of the lambda with arn {lambda_arn}")
            return True
        except botocore.exceptions.ClientError as e:
            print(e)
            return False

    def deploy(self, engine_resources: EngineResources, project_resources: ProjectResources,
               lambda_handler: str, runtime="python3.7", lambda_description: str = "Inoft Vocal Engine Deployment",
               lambda_timeout_seconds: int = 30, lambda_memory_size: int = 512, publish: bool = True) -> AWSBuildInfosBackendModel:

        has_modified_build_data = False

        # Retrieve or initialize the build data.
        build_data: Optional[AWSBuildInfosBackendModel] = engine_resources.accounts_data_dynamodb_client.get_infos_of_one_project_build(
            project_resources=project_resources, build_id="1d52c25e-bd69-4a66-95d5-23b0c747d974"
        )
        if build_data is None:
            build_data = AWSBuildInfosBackendModel(buildId=generate_uuid4())
            has_modified_build_data = True

        # Variables that will be used multiple times in the function
        expected_build_s3_key = f"{project_resources.project_owner_account_id}/{project_resources.account_project_id}/builds/build1.zip"
        expected_lambda_function_arn = f"{project_resources.account_project_id}-build-{build_data.buildName}"

        # Create and configure the Lambda function
        if build_data.lambdaArn is not None:
            if self.lambda_function_exist(function_name_or_arn=build_data.lambdaArn) is not True:
                build_data.lambdaArn = None
                has_modified_build_data = True

        # We do not use an elif statement here, to handle an non-existent lambda arn in the build data.
        if build_data.lambdaArn is None:
            if self.lambda_function_exist(function_name_or_arn=expected_lambda_function_arn) is True:
                build_data.lambdaArn = expected_lambda_function_arn
                has_modified_build_data = True

        if build_data.lambdaArn is not None:
            success = self._try_to_update_lambda_code(
                lambda_arn=build_data.lambdaArn, bucket_name=GeneratedCodeS3Client.PROJECTS_DATA_V1_BUCKET_NAME,
                object_key_name=expected_build_s3_key, handler_function_path=lambda_handler
            )
        else:
            # After creating the lambda function, we do not need to update
            # its code, because we defined its code while creating it.
            arn_created_lambda = self.create_lambda_function(
                bucket=GeneratedCodeS3Client.PROJECTS_DATA_V1_BUCKET_NAME, s3_key=expected_build_s3_key,
                function_name=f"{project_resources.account_project_id}-build-{build_data.buildName}",
                handler=lambda_handler, description=lambda_description,
                timeout=lambda_timeout_seconds, memory_size=lambda_memory_size,
                runtime=runtime, publish=publish
            )
            if arn_created_lambda is not None:
                build_data.lambdaArn = arn_created_lambda
                has_modified_build_data = True

        # Create and configure the API Gateway
        if build_data.apiGatewayId is not None:
            if self.rest_api_gateway_exist(build_data.apiGatewayId) is not True:
                build_data.apiGatewayId = None
                has_modified_build_data = True

        if build_data.apiGatewayId is not None:
            print(f"Using an existing API Gateway for deployment."
                  f"\n  --apiGatewayId:{build_data.apiGatewayId}")
        else:
            if build_data.lambdaArn is not None:
                api_id = self.create_api_gateway(lambda_arn=build_data.lambdaArn, api_gateway_name="the-api-noice", route_names=['{proxy+}'])
                if api_id is not None:
                    build_data.apiGatewayId = api_id
                    has_modified_build_data = True
                    print(f"Created a new API Gateway during deployment."
                          f"\n  --apiId:{api_id}")

        if has_modified_build_data is True:
            database_update_build_data_success = engine_resources.accounts_data_dynamodb_client.set_update_infos_of_one_project_build(
                project_resources=project_resources, build=build_data
            )

        return build_data


if __name__ == "__main__":
    engine_resources = EngineResources()
    account_resources = AccountResources(engine_resources=engine_resources)
    account_resources.account_username = "robinsonlabourdette"
    project_resources = ProjectResources(engine_resources=engine_resources, account_resources=account_resources,
                                         project_url="anvers1944", project_owner_account_username="robinsonlabourdette",
                                         project_owner_account_id="b1fe5939-032b-462d-92e0-a942cd445096")

    DeployHandler().deploy(engine_resources=engine_resources, project_resources=project_resources, lambda_handler="diagrams.lambda_handler")

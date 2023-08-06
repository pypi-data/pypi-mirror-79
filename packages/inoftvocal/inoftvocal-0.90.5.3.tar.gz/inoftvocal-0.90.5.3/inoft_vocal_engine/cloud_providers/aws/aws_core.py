import json
import logging
import time

import boto3
import botocore
import click
from boto.awslambda.exceptions import ResourceNotFoundException
from botocore.exceptions import ClientError, NoCredentialsError
from typing import List, Any, Tuple, Optional

from inoft_vocal_engine.cloud_providers.aws.core_clients import AwsCoreClients
from inoft_vocal_engine.safe_dict import SafeDict


class AwsCore(AwsCoreClients):
    def __init__(self, clients_to_load: List[int]):
        super().__init__(clients_to_load=clients_to_load)

        self.tags = {"framework": "InoftVocalFramework"}

        self._iam_role = None
        self._credentials_arn = None
        self._aws_account_id = None

        self._session_unix_time = None
        self._session_count_created_statement_ids = 0

        self.role_name = "InoftVocalFrameworkLambdaExecution"
        self.http_methods = ['ANY']

        self.default_description = "Created with the Inoft Vocal Framework"

    def create_s3_bucket_if_missing(self, bucket_name: str, region_name: str) -> bool:
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            return True
        except ClientError as e:
            click.echo(f"Trying to create a new S3 Bucket with name {click.style(text=bucket_name, fg='yellow', bold=True)}"
                       f" in region {click.style(text=region_name, fg='yellow', bold=True)}")
            available_regions_for_s3 = self.boto_session.get_available_regions(service_name="s3")
            if region_name not in available_regions_for_s3:
                raise Exception(f"The region {region_name} was not available for s3. Here is the available regions : {available_regions_for_s3}")

            self.s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": region_name})
            click.echo(f"Completed creation of the new bucket.")
            return False

    def _s3_prepare_upload_operation(self, bucket_name: str, region_name: str, access_should_be_public: bool = True) -> Tuple[bool, dict]:
        # If an error happen while uploading to S3, then the upload will not be
        # successful. We use that as our way to send a success response.
        extra_args = dict()
        if access_should_be_public is True:
            extra_args["ACL"] = "public-read"

        try:
            self.create_s3_bucket_if_missing(bucket_name=bucket_name, region_name=region_name)
            return True, extra_args
        except NoCredentialsError as e:
            click.echo(f"Almost there ! You just need to configure your AWS credentials."
                       f"\nYou can follow the official documentation (you will need to install the awscli by running pip install awscli) "
                       f"then go to https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration")
        except Exception as e:
            click.echo(f"Error while trying to create the S3 bucket before an upload operation : {e}")
        return False, extra_args

    def put_object_to_s3(self, object_item: Any, object_key_name: str, bucket_name: str, region_name: str, access_should_be_public: bool = True) -> bool:
        preparation_success, extra_kwargs = self._s3_prepare_upload_operation(
            bucket_name=bucket_name, region_name=region_name, access_should_be_public=access_should_be_public
        )
        if preparation_success is True:
            try:
                self.s3_client.put_object(Body=object_item, Bucket=bucket_name, Key=object_key_name, **extra_kwargs)
                return True
            except Exception as e:
                click.echo(f"Error while putting an object to the S3 bucket : {e}")
        return False

    def upload_file_to_s3(self, filepath: str, object_key_name: str, bucket_name: str, region_name: str, access_should_be_public: bool = True) -> bool:
        preparation_success, extra_args = self._s3_prepare_upload_operation(
            bucket_name=bucket_name, region_name=region_name, access_should_be_public=access_should_be_public
        )
        if preparation_success is True:
            try:
                self.s3_client.upload_file(Filename=filepath, Bucket=bucket_name, Key=object_key_name, ExtraArgs=extra_args)
                return True
            except Exception as e:
                click.echo(f"Error while uploading file to the S3 bucket : {e}")
        return False

    def remove_from_s3(self, file_name: str, bucket_name: str) -> bool:
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = int(e.response["Error"]["Code"])
            if error_code == 404:
                return False

        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=file_name)
            return True
        except (botocore.exceptions.ParamValidationError, botocore.exceptions.ClientError):
            return False

    def get_all_files_from_s3_folder(self, folderpath: str, bucket_name: str):
        response = self.s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=folderpath,
            MaxKeys=1000,
        )
        return response

    def get_lambda_function_arn(self, function_name_or_arn: str) -> Optional[str]:
        try:
            return SafeDict(self.lambda_client.get_function(FunctionName=function_name_or_arn)).get("Configuration").get("FunctionArn").to_str(default=None)
        except Exception as e:
            return None

    def lambda_function_exist(self, function_name_or_arn: str) -> bool:
        return True if self.get_lambda_function_arn(function_name_or_arn=function_name_or_arn) is not None else False

    def rest_api_gateway_exist(self, api_id: str) -> bool:
        try:
            response = self.api_gateway_client.get_rest_api(restApiId=api_id)
            return True
        except Exception as e:
            print(f"Rest API Gateway not found."
                  f"  --api_id:{api_id}"
                  f"  --error:{e}")
            return False

    def api_gateway_v2_url(self, api_id: str) -> str or None:
        try:
            return SafeDict(self.api_gateway_v2_client.get_api(ApiId=api_id)).get("ApiEndpoint").to_str(default=None)
        except Exception as e:
            return None

    def get_lambda_function_versions(self, function_name: str) -> list:
        try:
            response = self.lambda_client.list_versions_by_function(FunctionName=function_name)
            return response.get('Versions', list())
        except Exception as e:
            click.echo(f"Lambda function {function_name} not found. Error : {e}")
            return list()

    def create_lambda_function(self, bucket=None, s3_key: str = None, local_zip: bytes = None,
                               function_name: str = None, handler=None,
                               description: str = "Inoft Vocal Engine Deployment",
                               timeout: int = 30, memory_size: int = 512, publish: bool = True, runtime=None):
        """
        Given a bucket and key (or a local path) of a valid Lambda-zip, a function name and a handler, register that Lambda function.
        """
        kwargs = dict(
            FunctionName=function_name,
            Runtime=runtime,
            Role=self.credentials_arn,
            # "arn:aws:iam::631258222318:role/service-role/alexa_hackaton-cite-des-sciences_fakenews-challeng-role-ck3sxsyt",  # self.credentials_arn,
            # todo: make dynamic and create automaticly role if missing
            Handler=handler,
            Description=description,
            Timeout=timeout,
            MemorySize=memory_size,
            Publish=publish,
            Layers=[
                "arn:aws:lambda:eu-west-3:631258222318:layer:inoft-vocal-framework_v0-8dot3:2",
                # "arn:aws:lambda:eu-west-3:631258222318:layer:ffmpeg:2",
            ]
            # Those ARNs point to the required lambda layers to use the framework. Please do not modify them.
        )
        if local_zip is not None:
            kwargs['Code'] = {
                'ZipFile': local_zip
            }
        else:
            kwargs['Code'] = {
                'S3Bucket': bucket,
                'S3Key': s3_key
            }

        response = self.lambda_client.create_function(**kwargs)

        lambda_arn = response["FunctionArn"]
        version = response['Version']

        click.echo(f"Created new lambda function {function_name} with arn of {lambda_arn}")
        return lambda_arn

    def update_lambda_function_code(self, lambda_arn: str, object_key_name: str, bucket_name: str) -> dict:
        response = self.lambda_client.update_function_code(
            FunctionName=lambda_arn,
            S3Bucket=bucket_name,
            S3Key=object_key_name,
            Publish=True,
        )
        return response

    def update_lambda_function_configuration(self, function_name: str, handler_function_path: str = None,
                                             lambda_layers_arns: list = None) -> dict:
        kwargs = dict(FunctionName=function_name)
        if handler_function_path is not None:
            kwargs["Handler"] = handler_function_path
        if lambda_layers_arns is not None and len(lambda_layers_arns) > 0:
            kwargs["Layers"] = lambda_layers_arns

        response = self.lambda_client.update_function_configuration(**kwargs)
        return response

    def create_api_gateway(self, lambda_arn: str, api_gateway_name: str, route_names: List[str], description: str = None) -> Optional[str]:
        # todo: fix bug if id of api gateway is present in file, but the api has been deleted, it will not try to recreate it
        api_creation_response = SafeDict(self.api_gateway_client.create_rest_api(
            name=api_gateway_name, description=description or self.default_description
        ))
        api_id = api_creation_response.get("id").to_str(default=None)

        if api_id is not None:
            self.create_and_setup_api_methods(api_id=api_id, lambda_arn=lambda_arn, route_names=route_names)
            return api_id
        return None

    def get_resource_id_by_path(self, api_id: str, path: str) -> str:
        response = SafeDict(self.api_gateway_client.get_resources(restApiId=api_id))
        response_items = response.get("items").to_list()
        for resource in response_items:
            resource_safedict = SafeDict(resource)
            resource_path = resource_safedict.get("path").to_str(default=None)
            if resource_path is not None and resource_path == path:
                resource_id = resource_safedict.get("id").to_str(default=None)
                if resource_id is not None:
                    return resource_id
        return None

    def get_first_resource_id(self, api_id) -> str or None:
        response = SafeDict(self.api_gateway_client.get_resources(restApiId=api_id))
        response_items = response.get("items").to_list()
        for item in response_items:
            item_id = SafeDict(item).get("id").to_str(default=None)
            if item_id is not None:
                return item_id
        return None

    def _create_resource(self, api_id: str, path: str, parent_resource_id: str) -> str:
        resource_creation_response = SafeDict(self.api_gateway_client.create_resource(
            restApiId=api_id,
            parentId=parent_resource_id,
            pathPart=path
        ))
        created_resource_id = resource_creation_response.get('id').to_str(default=None)
        if created_resource_id is not None:
            # todo: when creating the api, add an AWS_PROXY (Lambda Proxy) integration
            pass
            """integration_creation_response = SafeDict(self.api_gateway_client.put_integration(
                restApiId=api_id,
                resourceId=created_resource_id,
                httpMethod='ANY',
                type='AWS_PROXY'
            ))"""
        return created_resource_id

    def put_method(api_id: str, parent_id: str, method: str, f: str, path: str = ""):
        apigateway = boto3.client('apigateway')

        apigateway.put_method(restApiId=api_id, resourceId=parent_id, httpMethod=method, authorizationType='NONE')

        apigateway.put_method_response(
            restApiId=api_id, resourceId=parent_id, httpMethod=method,
            statusCode="200", responseModels={"application/json": "Empty"})

        region = boto3.session.Session().region_name
        acct = boto3.client('sts').get_caller_identity().get('Account')
        uri = f"arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/arn:aws:" \
              f"lambda:{region}:{acct}:function:{f}/invocations"

        apigateway.put_integration(
            restApiId=api_id, resourceId=parent_id, httpMethod=method,
            type="AWS", integrationHttpMethod="POST", uri=uri
        )

        apigateway.put_integration_response(
            restApiId=api_id, resourceId=parent_id, httpMethod=method, statusCode="200",
            responseTemplates={'application/json': ""})

        source_arn = f"arn:aws:execute-api:{region}:{acct}:{api_id}/*/{method}/{path}"

        lambda_api = boto3.client('lambda')
        lambda_api.add_permission(
            FunctionName=f"arn:aws:lambda:{region}:{acct}:function:{f}",
            StatementId=uuid.uuid4().hex,
            Action="lambda:InvokeFunction",
            Principal="apigateway.amazonaws.com",
            SourceArn=source_arn
        )

    def _setup_method(self, api_id: str, created_resource_id: str, http_method: str, lambda_arn: str):
        # An authorizationType of NONE means that the method will have open access
        method_creation_response = SafeDict(self.api_gateway_client.put_method(
            restApiId=api_id, resourceId=created_resource_id, httpMethod=http_method, authorizationType="NONE")
        )

        region = self.boto_session.region_name
        account = boto3.client('sts').get_caller_identity().get('Account')
        uri = f"arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/arn:aws:" \
              f"lambda:{region}:{account}:function:{lambda_arn}/invocations"

        self.api_gateway_client.put_integration(
            restApiId=api_id, resourceId=created_resource_id, httpMethod='ANY',
            type='AWS', integrationHttpMethod='POST', uri=uri
        )

    def create_and_setup_api_methods(self, api_id: str, lambda_arn: str, route_names: List[str]):
        root_resource_id = self.get_resource_id_by_path(api_id=api_id, path='/')
        if root_resource_id is None:
            raise Exception(f"No route named / has been found in the api with id {api_id}")

        self._setup_method(api_id=api_id, created_resource_id=root_resource_id,
                           http_method="ANY", lambda_arn=lambda_arn)

        for route_name in route_names:
            self.boto_session.get_credentials()
            created_resource_id = self._create_resource(api_id=api_id, path=route_name, parent_resource_id=root_resource_id)
            if created_resource_id is not None:
                self._setup_method(api_id=api_id, created_resource_id=created_resource_id,
                                   http_method="ANY", lambda_arn=lambda_arn)

                """
                apigateway.put_integration(
                    restApiId=api_id, resourceId=parent_id, httpMethod=method,
                    type="AWS", integrationHttpMethod="POST", uri=uri
                )
    
                response = self.api_gateway_client.create_route(
                    ApiId=api_id,
                    AuthorizationType="None",
                    RouteKey=f"ANY /{route_name}",
                    # A space is required between the HTTP method and the /
                    Target=f"integrations/{integration_id}",
                )
                self.add_lambda_permission_to_call_api_resource(lambda_arn=lambda_arn, api_id=api_id, route_key=route_name)
                api_route_url = f"{api_gateway_root_url}/{route_name}"
                click.echo(f"Api route {click.style(route_name, fg='green')} creation complete accessible on {api_route_url}")
                # self.settings.get_set("deployment", {}).get_set("endpoints", {}).put(
                #    route_names_to_settings_keys[route_name], api_route_url).reset_navigated_dict()
                # We reset the navigated dict after a final put
                """

    def add_lambda_permission_to_call_api_resource(self, lambda_arn: str, api_id: str, route_key: str):
        response = self.lambda_client.add_permission(
            FunctionName=lambda_arn,
            StatementId=self.get_session_new_statement_id(),
            Action="lambda:InvokeFunction",
            Principal="apigateway.amazonaws.com",
            SourceArn=f"arn:aws:execute-api:{self.boto_session.region_name}:{self.aws_account_id}:{api_id}/*/*/{route_key}",
        )

    @property
    def iam_role(self) -> SafeDict:
        if self._iam_role is None:
            try:
                self._iam_role = SafeDict(self.iam_client.get_role(RoleName=self.role_name)["Role"])
            except botocore.exceptions.ClientError:
                # If a ClientError happened while getting the role, it means he do not exist.
                logging.debug(f"Creating {self.role_name} IAM Role..")

                attach_policy_obj = json.loads(self.attach_policy)
                assume_policy_obj = json.loads(self.assume_policy)

                self._iam_role = SafeDict(self.iam_client.create_role(
                    RoleName=self.role_name, AssumeRolePolicyDocument=self.assume_policy)["Role"])

                # create or update the role's policies if needed
                policy = self.iam_resource.RolePolicy(self.role_name, "inoft-vocal-permissions")
                try:
                    if policy.policy_document != attach_policy_obj:
                        logging.debug(f"Updating inoft-vocal-permissions policy on {self.role_name} IAM Role.")
                        policy.put(PolicyDocument=self.attach_policy)

                except botocore.exceptions.ClientError:
                    logging.debug(f"Creating inoft-vocal-permissions policy on {self.role_name} IAM Role.")
                    policy.put(PolicyDocument=self.attach_policy)

                role_policy_dict = self._iam_role.get("AssumeRolePolicyDocument").to_dict()
                if role_policy_dict != assume_policy_obj:
                    if (SafeDict(role_policy_dict["Statement"][0]).get("Principal").get("Service").to_any()
                            != assume_policy_obj["Statement"][0]["Principal"]["Service"]):
                        logging.debug(f"Updating assume role policy on {self.role_name} IAM Role.")
                        self.iam_client.update_assume_role_policy(RoleName=self.role_name,
                                                                  PolicyDocument=self.assume_policy)

        return self._iam_role

    @property
    def credentials_arn(self):
        if self._credentials_arn is None:
            self._credentials_arn = self.iam_role.get("Arn").to_str()
        return self._credentials_arn

    @credentials_arn.setter
    def credentials_arn(self, credentials_arn) -> None:
        self._credentials_arn = credentials_arn

    @property
    def aws_account_id(self) -> str:
        if self._aws_account_id is None:
            self._aws_account_id = boto3.client("sts").get_caller_identity().get("Account")
        return self._aws_account_id

    def get_session_new_statement_id(self) -> str:
        # No restriction is set on the statement id. To created my type of ids, i take the same unix
        # time across the session, and each time we generated a new statement id, i add 1 to the unix time.
        # Dumb and simple, but it assure that i will never have the same id twice.
        if self._session_unix_time is None:
            self._session_unix_time = time.time()
        self._session_count_created_statement_ids += 1

        # After turning the modified unix time into a string, we remove any point, that would have
        # been used to  separate the decimals, because AWS cannot accept a point in a id string.
        return str(self._session_unix_time + self._session_count_created_statement_ids).replace(".", "")

if __name__ == "__main__":
    Core().upload_file_to_s3(
        "F:\Inoft\hackaton cite des sciences 1\lambda_project\inoft_vocal_engine\cli\core\core_clients.py",
        "letestduframeworkinoft", "eu-west-3")


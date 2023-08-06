import os
import time
import zipfile
from pathlib import Path
from typing import Optional

import botocore
import click
from botocore.exceptions import ClientError
from click import ClickException

# todo: fix issue where when deploying we do not check if the api with the id found in the settings file do exit
from inoft_vocal_engine.cloud_providers.aws.aws_core import AwsCore
from inoft_vocal_engine.utils.paths import get_inoft_vocal_engine_root_path


class DeployHandler(AwsCore):
    def __init__(self):
        click.echo("Initializing AWS clients... (this can take a few seconds)")
        start_time = time.time()
        super().__init__(clients_to_load=[AwsCore.CLIENT_S3, AwsCore.CLIENT_LAMBDA, AwsCore.CLIENT_API_GATEWAY,
                                          AwsCore.CLIENT_IAM, AwsCore.CLIENT_STS, AwsCore.CLIENT_BOTO_SESSION])
        click.echo(f"Took {click.style(text=f'{round(time.time() - start_time, 2)}s', fg='white')} to initiate AWS clients")
        # todo: make the initialization even more asynchronous, by calling the handle function while the AWS ressources are initializing.
        #  Right now, the initialization of the resources are async, but we must wait for their completion in order to call the handle function.

    def deploy(self, lambda_files_root_folderpath: str, stage_name: str, bucket_name: str, bucket_region_name: str,
               lambda_name: str, lambda_handler: str, runtime="python3.7", upload_zip: bool = True,
               existing_zip_filepath: Optional[str] = None, lambda_description: str = "Inoft Vocal Engine Deployment",
               lambda_timeout_seconds: int = 30, lambda_memory_size: int = 512, publish: bool = True):

        # Make sure this isn't already deployed.
        """deployed_versions = self.get_lambda_function_versions(lambda_name)
        if len(deployed_versions) > 0:
            click.echo(f"This lambda function for this application is {click.style('already deployed', fg='green')}" +
                  f" If some part of the full deployment failed or you changed some resource name, and you want to do it again, type Y."
                  f" Otherwise, use the {click.style('inoft update', bold=True)} command")
            if not click.confirm("Do you want to redo the deployment ?"):
                click.echo(f"Ok ! Remember to use the {click.style('inoft update', bold=True)} command !")
                exit()
        """

        zip_filepath, upload_success = None, None
        if upload_zip is True:
            if existing_zip_filepath is None:
                # Create the Lambda Zip
                zip_filepath = self.create_package(to_zip=True, to_s3=False,
                                                   app_folder_path=lambda_files_root_folderpath,
                                                   stage_name=stage_name, bucket_name=bucket_name, bucket_region_name=bucket_region_name)
            else:
                if not os.path.isfile(existing_zip_filepath):
                    raise Exception(f"Existing app project zip file do not exist at filepath : {existing_zip_filepath}")
                zip_filepath = existing_zip_filepath

            # Upload it to S3
            click.echo("Uploading the lambda zip file to S3")
            upload_success = self.upload_file_to_s3(filepath=zip_filepath, object_key_name=Path(zip_filepath).name,
                                               bucket_name=bucket_name, region_name=bucket_region_name)
            if not upload_success:
                raise ClickException("Unable to upload to S3. Look in the logs what caused the errors,"
                                     " and modify your app_settings file in order to fix the issue."
                                     "\nCommon issues include :"
                                     "\n - Not having setup your credentials correctly (run the command : aws configure)"
                                     "\n - Trying to use a S3 bucket name that is not available."
                                     "\n - Having modified the app_settings file, but not have saved it with CTRL+S")
            click.echo("Uploading completed.")

        src_folderpath = os.path.join(get_inoft_vocal_engine_root_path(), "web_interface/static/dist")
        self.upload_folder_to_s3(src_folderpath=src_folderpath, s3_target_folderpath="prod/static/dist",
                                 bucket_name=bucket_name, bucket_region_name=bucket_region_name)

        return True

        # Remove the project zip from S3.
        if not source_zip:
            self.remove_uploaded_zip()

    def deploy_from_s3_files(self, s3_bucket_name: str, s3_dirpath: str):
        self.s3_client
        try:
            lambda_arn = self.get_lambda_function_arn(function_name_or_arn=lambda_name)
            click.echo(f"Using the existing lambda function {lambda_name}")
            if upload_success is True:
                self.update_lambda_function_code(lambda_arn=lambda_arn, object_key_name=Path(zip_filepath).name, bucket_name=bucket_name)
                self.update_lambda_function_configuration(function_name=lambda_arn, handler_function_path=lambda_handler)
                click.echo(f"Updated the code of the lambda with arn {lambda_arn}")

        except botocore.exceptions.ClientError:
            try:
                lambda_arn = self.create_lambda_function(bucket=bucket_name, s3_key=Path(zip_filepath).name, function_name=lambda_name,
                                                         handler=lambda_handler, description=lambda_description,
                                                         timeout=lambda_timeout_seconds, memory_size=lambda_memory_size,
                                                         runtime=runtime, publish=publish)
                click.echo(f"Created the lambda function : {lambda_name}")
            except Exception as e:
                click.echo(f"Error while updating the function by giving it a S3 path. Trying to update the"
                           f"function with a byte_stream of the zip file of the deployment package : {e}")

                with open(zip_filepath, mode="rb") as file_stream:
                    byte_stream = file_stream.read()

                lambda_arn = self.create_lambda_function(local_zip=byte_stream, function_name=lambda_name,
                                                         handler=lambda_handler, description=lambda_description,
                                                         timeout=lambda_timeout_seconds, memory_size=lambda_memory_size,
                                                         runtime=runtime, publish=publish)
                click.echo(f"Created the lambda function : {lambda_name}")

        # Create and configure the API Gateway
        need_to_create_api = False
        # api_gateway_id = self.settings.settings.get("deployment").get("apiGatewayId").to_str(default=None)
        api_gateway_id = "1g9v1ilt6b"  # None  # todo: store the id of the api in a database
        if api_gateway_id is None or self.rest_api_gateway_exist(api_gateway_id) is None:
            api_id = self.create_api_gateway(lambda_arn=lambda_arn, lambda_name=lambda_name, route_names=['{proxy+}'])
            click.echo(f"Created a new {click.style(text='API Gateway', bold=True)}")
            print(f"api_id = {api_id}")
            # self.settings.settings.get("deployment").put("apiGatewayId", api_id)
            # self.settings.save_settings()
        else:
            click.echo(f"Using the existing ApiGatewayV2 with id {click.style(text=api_gateway_id, bold=True, fg='green')}")


    def upload_folder_to_s3(self, src_folderpath: str, s3_target_folderpath: str, bucket_name: str, bucket_region_name: str):
        for root_dirpath, dirs, filenames in os.walk(src_folderpath, topdown=True):
            relative_root_dirpath = root_dirpath.replace(src_folderpath, "").replace("\\", "/").lstrip("/")
            # We need to remove potential leading backslashes and slashes, otherwise, when we will use the os.path.join
            # function, it will remove the first element of the path we are trying to combine the relative_root_dirpath.
            # For example, if we did os.path.join("prod", "\\folder\\file.py") we would end up with \\folder\\file.py
            # where as doing os.path.join("prod", "folder\\file.py") will give us prod\\folder\\file.py

            for filename in filenames:
                current_file_filepath = f"{root_dirpath}/{filename}"
                current_file_relative_filepath = f"{relative_root_dirpath}/{filename}"

                s3_object_key_name = f"{s3_target_folderpath}{current_file_relative_filepath}"
                self.upload_file_to_s3(filepath=current_file_filepath, object_key_name=s3_object_key_name,
                                  bucket_name=bucket_name, region_name=bucket_region_name)
                print(f"- {current_file_filepath}  - S3 uploaded to path {s3_object_key_name}")


    def create_package(self, app_folder_path: str, to_zip: bool = False, to_s3: bool = False, stage_name: Optional[str] = None,
                       bucket_name: Optional[str] = None, bucket_region_name: Optional[str] = None) -> str:
        if to_zip is False and to_s3 is False:
            raise Exception(f"To create or upload a package you must set the to_zip and/or the to_s3 argument to True.")

        archive_destination_filepath = os.path.join(Path(app_folder_path).parent, f"{Path(app_folder_path).name}.zip")
        click.echo(f"Making an archive from all the files and folders in {app_folder_path} to {archive_destination_filepath}")

        folders_names_to_excludes = [".aws-sam", ".idea", ".git", "__pycache__", "venv", "dist", "node_modules", "lambda_layer",
                                     "speech_synthesis\\export", "speech_synthesis\\polly\\project_data", "libs"]
        # todo: re-include node_modules for production

        has_found_engine_in_project_files = False
        zip_object = None if to_zip is not True else zipfile.ZipFile(file=archive_destination_filepath, mode="w")
        # has_found_framework_in_project_files = False

        if to_s3 is True:
            print(f"Uploading of files starting...  - bucket_name:{bucket_name}  - bucket_region_name:{bucket_region_name}")
        if to_zip is True:
            print(f"Zipping of files starting...   - archive_destination_filepath:{archive_destination_filepath}")

        # Include the projects files
        for root_dirpath, dirs, filenames in os.walk(app_folder_path, topdown=True):
            # The topdown arg allow use to modify the dirs list in the walk, and so we can easily exclude folders.

            # dirs[:] = [dirpath for dirpath in dirs if Path(dirpath).name not in folders_names_to_excludes]
            # This code would only check if the name of the directory is found in the folders names to exclude

            # Where the code below, will check, if the names or paths of all the folder names or paths to exclude,
            # have been found in the dirpath. This approach allow to check for both folder name, and folder paths.
            for folder_name in folders_names_to_excludes:
                for dirname in dirs:
                    dirpath = os.path.join(root_dirpath, dirname)
                    if folder_name in dirpath:
                        dirs.remove(dirname)

            # if Path(root_dirpath).name == "inoft_vocal_engine":
            #    has_found_engine_in_project_files = True

            relative_root_dirpath = root_dirpath.replace(app_folder_path, "").replace("\\", "/").lstrip("/")
            # We need to remove potential leading backslashes and slashes, otherwise, when we will use the os.path.join
            # function, it will remove the first element of the path we are trying to combine the relative_root_dirpath.
            # For example, if we did os.path.join("prod", "\\folder\\file.py") we would end up with \\folder\\file.py
            # where as doing os.path.join("prod", "folder\\file.py") will give us prod\\folder\\file.py
            relative_root_dirpath = f"inoft_vocal_engine/{relative_root_dirpath}"

            for filename in filenames:
                current_file_filepath = f"{root_dirpath}/{filename}"
                current_file_relative_filepath = f"{relative_root_dirpath}/{filename}"
                current_file_print_log = f"- {current_file_filepath}"

                if to_zip is True:
                    zip_object.write(filename=current_file_filepath,
                                     arcname=current_file_relative_filepath)
                    current_file_print_log += f"  - ZIP added to path {current_file_relative_filepath}"

                if to_s3 is True:
                    s3_object_key_name = f"{stage_name}/{current_file_relative_filepath}"
                    self.upload_file_to_s3(filepath=current_file_filepath, object_key_name=s3_object_key_name,
                                      bucket_name=bucket_name, region_name=bucket_region_name)
                    current_file_print_log += f"  - S3 uploaded to path {s3_object_key_name}"

                print(current_file_print_log)

            # todo: when doing a redeploy, check that the lambda layer used, is the right layer for the current framework version

            """
            if has_found_engine_in_project_files is False:
                # On the condition that we have not found the engine in the project files. This function exist both for development sake,
                # where i can deploy with a dev version of the engine without having to publish to pip, while stile using the command line
                # interface from the pip package. And also since the engine (and its correct version) will be included in the deployment
                # package, so that if an user download an app deployed in a different version that the current version of the framework he
                # is using, the version of the framework that will be used will be the one included in its package, not the one installed.

                # We will include the inoft_vocal_engine himself (he is not included in the lambda layers)
                # I do not include the framework in the lambda layer, because it would be weird for someone to update the framework,
                # do a redeploy, and not have upgraded its deploy. Where as we can check if its layer is the right layer for the version
                # of his framework. And mostly because it would be annoying for me to recreate a new lambda layer on each update of the
                # framework, and that he is light enough to be included in the package and the increase in upload time to not be noticeable ;)
                inoft_vocal_engine_folder_path = os.path.dirname(os.path.realpath(inoft_vocal_engine.__file__))
                for root_dirpath, dirs, filenames in os.walk(inoft_vocal_engine_folder_path):
                    relative_dirpath_with_root_included = root_dirpath.replace(str(Path(inoft_vocal_engine_folder_path).parent), "")
                    # We only replace the parent of the framework folder path, because we want it to be in its inoft_vocal_engine folder.
                    for filename in filenames:
                        zip_object.write(filename=os.path.join(root_dirpath, filename),
                                         arcname=os.path.join(relative_dirpath_with_root_included, filename))
            """


        # from shutil import make_archive
        # zip_filepath = make_archive(base_name=archive_destination_filepath_without_extension, format="zip", root_dir=app_folder_path)
        click.echo(f"Archive completed at {click.style(text=archive_destination_filepath, bold=True)}")

        # Warn if this is too large for Lambda.
        file_stats = os.stat(archive_destination_filepath)
        if file_stats.st_size > 52428800:
            click.echo("Warning: Application zip package is likely to be too large for AWS Lambda. Try to make it smaller")

        return archive_destination_filepath

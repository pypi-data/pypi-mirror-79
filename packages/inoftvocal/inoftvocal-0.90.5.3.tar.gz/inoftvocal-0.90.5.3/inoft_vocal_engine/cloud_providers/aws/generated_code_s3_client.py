import os
from dataclasses import dataclass
from datetime import datetime
from tempfile import TemporaryFile
from typing import Optional, List

import inoft_vocal_engine
from inoft_vocal_engine.cloud_providers.aws.aws_core import AwsCore
from inoft_vocal_engine.cloud_ressources.account_resources import AccountResources
from inoft_vocal_engine.cloud_ressources.engine_resources import EngineResources
from inoft_vocal_engine.cloud_ressources.project_resources import ProjectResources
from inoft_vocal_engine.safe_dict import SafeDict
from uuid import uuid4
from inoft_vocal_engine.utils.paths import get_engine_temp_path


@dataclass
class RetrievedS3File:
    Key: str
    LastModified: datetime
    ETag: str
    Size: float
    StorageClass: str
    FileContent: Optional[str] = None


class GeneratedCodeS3Client(AwsCore):
    PROJECTS_DATA_V1_BUCKET_NAME = "inoft-vocal-engine-web-test"

    def __init__(self):
        super().__init__(clients_to_load=[AwsCore.CLIENT_S3])
        self.temp_dirpath = get_engine_temp_path()

    def _make_new_temp_filepath(self) -> os.path:
        # We use a UUID in the filepath, because otherwise, if the name of the temp_app_code file was unique,
        # if the code is executed at the same time by multiple users, the temporary file of one user that is
        # being uploaded and has not yet been deleted, might be overridden by the temporary file of another user.
        temp_filepath = os.path.join(self.temp_dirpath, f"temp_app_code_{str(uuid4())}.py")
        while os.path.exists(temp_filepath):
            # If the filepath already exists (which would be weird since we use an unique uuid in
            # the filepath), we generate a new temp_filepath until we found one that do not yet exists.
            temp_filepath = self._make_new_temp_filepath()
            print(f"Temp path is a duplicate. Creating a new one.\n  --temp_filepath:{temp_filepath}")
        return temp_filepath

    def _make_new_temp_build_dirpath(self, project_resources: ProjectResources) -> os.path:
        temp_build_dirpath = os.path.join(
            self.temp_dirpath, project_resources.project_owner_account_id, project_resources.account_project_id, "builds", str(uuid4())
        )
        while os.path.exists(temp_build_dirpath):
            temp_build_dirpath = self._make_new_temp_build_dirpath(project_resources=project_resources)
            print(f"Build dir path is a duplicate. Creating a new one.\n  --temp_build_dirpath:{temp_build_dirpath}")
        return temp_build_dirpath

    @staticmethod
    def _make_s3_project_folder_key_name(project_resources: ProjectResources) -> str:
        return f"{project_resources.project_owner_account_id}/{project_resources.account_project_id}"

    @staticmethod
    def _make_archive_filename_from_s3_key(project_resources: ProjectResources, s3_key: str) -> str:
        filepath_before_and_with_account_id, filepath_after_account_id = (
            s3_key.split(project_resources.project_owner_account_id, maxsplit=1)
        )
        if len(filepath_after_account_id) == 0:
            filepath_after_account_id = filepath_before_and_with_account_id

        filepath_before_and_with_project_id, filepath_after_project_id = (
            filepath_after_account_id.split(project_resources.account_project_id, maxsplit=1)
        )
        if len(filepath_after_project_id) == 0:
            filepath_after_project_id = filepath_before_and_with_project_id

        filepath_before_and_with_files_folder, filepath_after_files_folder = (
            filepath_after_project_id.split("files", maxsplit=1)
        )
        if len(filepath_after_files_folder) == 0:
            filepath_after_files_folder = filepath_before_and_with_files_folder

        filepath_after_files_folder: str
        filepath_after_files_folder = filepath_after_files_folder.lstrip("/")

        return filepath_after_files_folder

    def upload_app_code(self, project_resources: ProjectResources, app_code: str, key_filename: str):
        # todo: replace the use of real temporary file, by the tempfile module
        temp_dirpath = os.path.join(os.path.dirname(os.path.realpath(inoft_vocal_engine.__file__)), "tmp")
        if not os.path.isdir(temp_dirpath):
            os.makedirs(temp_dirpath)

        temp_filepath = self._make_new_temp_filepath()

        with open(temp_filepath, mode="w+", encoding="utf-8") as temp_file:
            temp_file.write(app_code)

        # todo: make object key name dynamic based on account and project id
        s3_object_key_name = f"{self._make_s3_project_folder_key_name(project_resources=project_resources)}/files/{key_filename}"
        self.upload_file_to_s3(
            filepath=temp_filepath, object_key_name=s3_object_key_name,
            bucket_name=self.PROJECTS_DATA_V1_BUCKET_NAME, region_name="eu-west-3",
            access_should_be_public=True
        )
        # When the temporary file is uploaded to S3, we remove it.
        os.remove(temp_filepath)

    def get_code_of_one_file(self, file_bucket_key: str) -> Optional[str]:
        # todo: optimize this shit code (use safedict, make more precise catches, etc)
        response = self.s3_client.get_object(Bucket=self.PROJECTS_DATA_V1_BUCKET_NAME, Key=file_bucket_key)
        if isinstance(response, dict):
            body = response.get('Body', None)
            if body is not None:
                try:
                    body = body.read().decode('utf-8')
                    return body
                except Exception as e:
                    print(e)
        return None

    def get_infos_of_all_build_files(self, project_resources: ProjectResources) -> Optional[List[RetrievedS3File]]:
        s3_project_folder_key_name = f"{self._make_s3_project_folder_key_name(project_resources=project_resources)}/files"
        response = self.get_all_files_from_s3_folder(
            bucket_name=self.PROJECTS_DATA_V1_BUCKET_NAME,
            folderpath=s3_project_folder_key_name
        )
        if isinstance(response, dict):
            contents: Optional[List[dict]] = response.get('Contents', None)
            if contents is not None:
                output_retrieved_files_objects: List[RetrievedS3File] = list()
                for item in contents:
                    output_retrieved_files_objects.append(RetrievedS3File(**item))
                return output_retrieved_files_objects
        return None

    def get_contents_of_all_build_files(self, project_resources: ProjectResources) -> Optional[List[RetrievedS3File]]:
        files_data = self.get_infos_of_all_build_files(project_resources=project_resources)
        if files_data is not None:
            # At this point, the files_data only contains the infos of each file without its data.
            for file_info in files_data:
                if file_info.Key is not None:
                    file_content = self.get_code_of_one_file(file_bucket_key=file_info.Key)
                    if file_content is not None:
                        file_info.FileContent = file_content

            # After our loop, if we have been able to retrieve the contents,
            # the files_data object also contains the content of each file.
            return files_data
        return None

    def generate_zip_from_build_files(self, project_resources: ProjectResources) -> Optional[str]:
        from tempfile import SpooledTemporaryFile
        import zipfile

        files_data_with_content = self.get_contents_of_all_build_files(project_resources=project_resources)
        if files_data_with_content is not None:
            build_zip_file_key_name = f"{self._make_s3_project_folder_key_name(project_resources=project_resources)}/builds/build1.zip"

            temp_build_dirpath = self._make_new_temp_build_dirpath(project_resources=project_resources)
            temp_build_files_dirpath = os.path.join(temp_build_dirpath, "files")
            os.makedirs(temp_build_files_dirpath)
            # This single makedirs will create the dirs for the temp_build_dirpath and temp_build_files_dirpath variables.
            temp_build_zipfile_filepath = os.path.join(temp_build_dirpath, "build.zip")

            success = False
            try:
                with open(temp_build_zipfile_filepath, mode="w+") as temp_zipfile:
                    with zipfile.ZipFile(temp_build_zipfile_filepath, 'w', zipfile.ZIP_DEFLATED) as archive:
                        for file in files_data_with_content:
                            if file.FileContent is not None:
                                archive_filename = self._make_archive_filename_from_s3_key(project_resources=project_resources, s3_key=file.Key)

                                temp_archive_nested_file_filename = os.path.join(temp_build_files_dirpath, archive_filename)
                                with open(temp_archive_nested_file_filename, "w+") as temp_nested_file:
                                    # For some reasons, the \r in the FileContent do not pose any issues in the string
                                    # representation of PyCharm, but will double each new line when writing the data to a file.
                                    # Removing all the \r fix the issue without causing any loss of integrity to the file data.
                                    temp_nested_file.write(file.FileContent.replace("\r", ""))
                                    # os.chmod(temp_archive_nested_file_filename, 0o777)  # Not necessary to set the file permissions

                                archive.write(filename=temp_archive_nested_file_filename, arcname=archive_filename)

                    # Reset file pointer
                    temp_zipfile.seek(0)

                # os.chmod(temp_build_zipfile_filepath, 0o777)  # Not necessary to set the file permissions
                success = self.upload_file_to_s3(
                    filepath=temp_build_zipfile_filepath, object_key_name=build_zip_file_key_name,
                    bucket_name=self.PROJECTS_DATA_V1_BUCKET_NAME, region_name="eu-west-3",
                    access_should_be_public=True
                )
            except Exception as e:
                print(e)
            finally:
                from shutil import rmtree
                # Delete the folder and all its content
                # (os.remove is only done to remove a single file)
                rmtree(temp_build_dirpath)

            print(f"success = {success}")
            if success is True:
                return build_zip_file_key_name
        return None


if __name__ == "__main__":
    engine_resources = EngineResources()
    account_resources = AccountResources(engine_resources=engine_resources)
    account_resources.account_username = "robinsonlabourdette"
    project_resources_ = ProjectResources(engine_resources=engine_resources, account_resources=account_resources,
                                         project_url="anvers1944", project_owner_account_username="robinsonlabourdette",
                                         project_owner_account_id="b1fe5939-032b-462d-92e0-a942cd445096")

    GeneratedCodeS3Client().generate_zip_from_build_files(project_resources=project_resources_)


"""
                            # with TemporaryFile() as tmp2:
                                # tmp2.write(bytes(file.FileContent))
                                # archive.write(filename=tmp2.name)
                            # todo: fix issue where the files inside the zip are saved in readonly mode, and so
                            #  will not be able to be accessed by Lambda, until we manually modify it in the console."""
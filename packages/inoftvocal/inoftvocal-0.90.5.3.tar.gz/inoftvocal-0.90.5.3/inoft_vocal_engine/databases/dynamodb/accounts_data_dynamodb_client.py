import time
from dataclasses import asdict
from typing import Any, Optional, List, Dict, Tuple
from boto3.exceptions import ResourceNotExistsError
from boto3.dynamodb.conditions import Attr, Key
from pydantic import BaseModel, validator, ValidationError

from inoft_vocal_engine.databases.dynamodb.dynamodb_core import DynamoDbCoreAdapter, PrimaryIndex, GlobalSecondaryIndex, Response
from inoft_vocal_engine.databases.dynamodb.dynamodb_utils import Utils
from inoft_vocal_engine.safe_dict import SafeDict
from inoft_vocal_engine.web_interface.auth.models import AuthToken, AccountData


class InstanceInfoDatabaseItem(BaseModel):
    projectId: str
    instanceName: str
    instanceDescription: Optional[str] = None
    instanceId: Optional[str] = None

    @validator('instanceId', always=True)
    def make_uuid_if_missing(cls, value):
        if value is not None:
            return value
        else:
            from uuid import uuid4
            instance_id = str(uuid4())
            print(f"Initializing new instance --instanceId:{instance_id}")
            return instance_id

    def to_database(self) -> dict:
        return self.dict(exclude={"projectId"})

class ProjectDatabaseItem(BaseModel):
    """ To be used in the projects dict of the AccountDatabaseItem """
    projectName: str
    projectPrimaryUrl: str
    projectDescription: Optional[str] = None
    instancesInfos: Optional[Dict[str, InstanceInfoDatabaseItem]] = dict()
    accountProjectId: Optional[str] = None

    @validator('accountProjectId', always=True)
    def make_uuid_if_missing(cls, value):
        if value is not None:
            return value
        else:
            from uuid import uuid4
            account_project_id = str(uuid4())
            print(f"Initializing new project --accountProjectId:{account_project_id}")
            return account_project_id

class AccountDatabaseItem(BaseModel):
    email: str
    username: str
    encryptedPassword: str
    accountId: Optional[str] = None
    authTokens: Optional[list] = list()
    projects: Optional[dict] = dict()
    permissionsGrantedToOtherAccounts: Optional[Dict[str, List[str]]] = dict()
    permissionsGivenToAccount: Optional[Dict[str, List[str]]] = dict()
    projectsUrlsToIds: Optional[Dict[str, str]] = list()
    sharedProjectsIds: Optional[List[str]] = list()
    # todo: remove use of fields that were used when this class was a dataclass instead of a BaseModel

    @validator('accountId', always=True)
    def make_uuid_if_missing(cls, value):
        if value is not None:
            return value
        else:
            from uuid import uuid4
            account_id = str(uuid4())
            print(f"Initializing new account --accountId:{account_id}")
            return account_id

class AWSBuildInfosDatabaseModel(BaseModel):
    provider: str = "AWS"
    buildName: str = "development"
    lambdaArn: Optional[str] = None
    apiGatewayId: Optional[str] = None

class AWSBuildInfosBackendModel(AWSBuildInfosDatabaseModel):
    buildId: str

    def to_database_model(self) -> AWSBuildInfosDatabaseModel:
        return AWSBuildInfosDatabaseModel(
            provider=self.provider,
            buildName=self.buildName,
            lambdaArn=self.lambdaArn,
            apiGatewayId=self.apiGatewayId
        )



class UsersDynamoDBClient(DynamoDbCoreAdapter):
    AUTH_TOKEN_SECONDS_TIMEOUT = 86400  # 24 hours in seconds

    def __init__(self, table_name: str, region_name: str):
        primary_index = PrimaryIndex(hash_key_name="accountId", hash_key_variable_python_type=str)
        globals_secondary_indexes = [
            GlobalSecondaryIndex(hash_key_name="username", hash_key_variable_python_type=str, projection_type="ALL"),
            GlobalSecondaryIndex(hash_key_name="email", hash_key_variable_python_type=str, projection_type="ALL"),
        ]
        super().__init__(table_name=table_name, region_name=region_name, primary_index=primary_index,
                         global_secondary_indexes=globals_secondary_indexes, create_table=True)
        # The table should exist in only one copy, which is why its name and region is hardcoded

    def put_new_account(self, account_item: AccountDatabaseItem) -> AccountDatabaseItem:
        account_item_dict = asdict(account_item)
        self._put_item_dict(item_dict=account_item_dict)
        print(f"Finished creation of new account."
              f"  --item{account_item_dict}"
              f"  --time:{time.time()}")
        return account_item

    def add_project_to_account(self, account_id: str, project_item: ProjectDatabaseItem,
                               project_secondary_urls: Optional[List[str]] = None):
        # todo: before creating a project, check if no project in the account has the same primary url

        project_item_dict_values = project_item.dict()
        account_item_set_response = self._add_update_data_element_to_map(
            key_name="accountId", key_value=account_id,
            object_path_elements={'projects': dict, project_item.accountProjectId: str},
            element_values=project_item_dict_values
        )
        if account_item_set_response is None:
            print(f"Error while adding new project item to an account."
                  f"  --account_id:{account_id}"
                  f"  --key:{project_item.projectName}"
                  f"  --item:{project_item_dict_values}"
                  f"  --time:{time.time()}")
            return False
        else:
            if project_secondary_urls is None:
                # If we have only one element to add to a map, the add_data_element_to_map is more efficient in processing power for the server
                # than add_multiple_data_elements_to_map. Otherwise the add_multiple_data_elements_to_map is more efficient in database accesses.
                self._add_update_data_element_to_map(
                    key_name="accountId", key_value=account_id,
                    object_path_elements={'projectsUrlsToIds': dict, project_item.projectName: str},
                    element_values=project_item.accountProjectId
                )
            else:
                from inoft_vocal_engine.databases.dynamodb.dynamodb_core import DynamoDBMapObjectSetter
                project_secondary_urls.append(project_item.projectName)
                project_urls = project_secondary_urls
                objects_setters: List[DynamoDBMapObjectSetter] = list()
                for url in project_urls:
                    objects_setters.append(DynamoDBMapObjectSetter(object_path='projectsUrlsToIds', map_key=url,
                                                                   value_to_set=project_item.accountProjectId))
                self._add_update_multiple_data_elements_to_map(key_name="accountId", key_value=account_id, objects_setters=objects_setters)

            print(f"Added new project item to an account."
                  f"  --account_id:{account_id}"
                  f"  --key:{project_item.projectName}"
                  f"  --item:{project_item_dict_values}"
                  f"  --time:{time.time()}")
            return True

    def add_instance_infos_to_account(self, account_id: str, instance_infos_item: InstanceInfoDatabaseItem) -> bool:
        instance_infos_item_dict_values = instance_infos_item.to_database()
        instance_infos_update_response = self._add_update_data_element_to_map(
            key_name="accountId", key_value=account_id, element_values=instance_infos_item_dict_values,
            object_path_elements={
                'projects': dict, instance_infos_item.projectId: dict,
                'instancesInfos': dict, instance_infos_item.instanceId: dict
            }
        )
        if instance_infos_update_response is not None:
            return True
        else:
            print(f"Error while adding new instance infos item to an account."
                  f"  --account_id:{account_id}"
                  f"  --key:{instance_infos_item.projectId}"
                  f"  --item:{instance_infos_item_dict_values}"
                  f"  --time:{time.time()}")
            return False

    # todo: decide if the password validation should be directly done in the database queries ?
    def get_account_by_username(self, username: str, fields_to_get: list) -> dict:
        return self._query_single_item_by_key(index_name="username", key_name="username", key_value=username, fields_to_get=fields_to_get)

    def get_account_by_email(self, email: str, fields_to_get: list) -> dict:
        return self._query_single_item_by_key(index_name="email", key_name="email", key_value=email, fields_to_get=fields_to_get)

    def check_permissions_on_account_project(self, project_owner_account_username: str, requester_account_id: str,
                                             permissions_to_check: List[str], fields_to_get: List[str]):

        requester_expected_permissions_map_path = f"permissionsGrantedToOtherAccounts.{requester_account_id}"
        # We store this string in a variable, just to not have to create it multiple times in the permissions loop

        filter_expression = Attr(requester_expected_permissions_map_path).exists()
        for permission in permissions_to_check:
            filter_expression = self._add_to_filter_expression(
                expression=filter_expression,
                condition=Attr(requester_expected_permissions_map_path).contains(permission)
            )

        response = self._query_by_key(
            index_name="username", key_name="username", key_value=project_owner_account_username,
            filter_expression=filter_expression, fields_to_get=fields_to_get
        )
        return response

    def get_account_permissions_granted_to_other_accounts_by_username(self, owner_account_username: str,
                                                                      account_id_to_get_permissions_for: str) -> Tuple[dict, bool]:

        response = self._query_for_account(index_name="username", key_name="username", key_value=owner_account_username,
                                           fields_to_get=[f"permissionsGrantedToOtherAccounts.{account_id_to_get_permissions_for}"])
        return response

    def remove_old_auth_tokens(self, account_id: str, fields_to_get: List[str]) -> AccountData:
        # account_data, account_been_found \
        # todo: optimize this code, because currently when logging, we have multiple accesses on the users database
        get_account_response = self._query_by_key(key_name="accountId", key_value=account_id, fields_to_get=fields_to_get)

        if len(get_account_response.items) > 0:
            account_data = AccountData(**get_account_response.items[0])
            indexes_tokens_to_remove = list()

            current_time = time.time()
            if account_data.authTokens is not None:
                for i, auth_token in enumerate(account_data.authTokens):
                    try:
                        if current_time > auth_token.creationTimestamp + self.AUTH_TOKEN_SECONDS_TIMEOUT:
                            indexes_tokens_to_remove.append(i)
                    except Exception as e:
                        indexes_tokens_to_remove.append(i)
                        print(f"Auth toke {auth_token} was invalid and will be removed. It has caused the following error {e}")

            if len(indexes_tokens_to_remove) > 0:
                update_expression = "REMOVE "
                for i, token_index_in_database_list in enumerate(indexes_tokens_to_remove):
                    update_expression += f"authTokens[{token_index_in_database_list}]"
                    if i + 1 < len(indexes_tokens_to_remove):
                        update_expression += ", "

                self._remove_data_elements_from_list(key_name="accountId", key_value=account_id,
                                                     list_object_path="authTokens", indexes_to_remove=indexes_tokens_to_remove)

                for i_old_token in indexes_tokens_to_remove:
                    account_data.authTokens.pop(i_old_token)
            return account_data

    def add_auth_token(self, account_id: str) -> str:
        from uuid import uuid4
        auth_token = AuthToken(token=str(uuid4()), creationTimestamp=int(time.time()))
        self._add_data_elements_to_list(key_name="accountId", key_value=account_id,
                                        object_path="authTokens", element_values=[auth_token.dict()])
        return auth_token.token

    def get_account_project_id_by_project_url(self, project_url: str, account_id: Optional[str] = None, account_username: Optional[str] = None) -> Optional[str]:
        kwargs = {}
        if account_id is not None:
            kwargs["key_name"] = "accountId"
            kwargs["key_value"] = account_id
        elif account_username is not None:
            kwargs["key_name"] = "username"
            kwargs["key_value"] = account_username
            kwargs["index_name"] = "username"

        response_items = self._query_by_key(**kwargs, query_limit=1,
            fields_to_get=[f"projectsUrlsToIds.{project_url}"],
            filter_expression=Attr(f"projectsUrlsToIds.{project_url}").exists()
        ).items

        if len(response_items) > 0:
            account_project_id = SafeDict(response_items[0]).get("projectsUrlsToIds").get(project_url).to_str(default=None)
            return account_project_id

    def get_project_by_project_url(self, account_id: str, project_url: str) -> Optional[ProjectDatabaseItem]:
        account_project_id = self.get_account_project_id_by_project_url(account_id=account_id, project_url=project_url)

        if account_project_id is not None:
            response_items = self._query_by_key(
                key_name="accountId", key_value=account_id,
                fields_to_get=[f"projects.{account_project_id}"],
                filter_expression=Attr(f"projects.{account_project_id}").exists()
            ).items
            if len(response_items) > 0:
                project_dict = SafeDict(response_items[0]).get("projects").get(account_project_id).to_dict(default=None)
                if project_dict is not None:
                    project_instance = ProjectDatabaseItem(**project_dict)
                    return project_instance

    def _get_all_owned_projects_of_account(self, key_name: str, key_value: str, index_name: Optional[str] = None) -> Optional[List[ProjectDatabaseItem]]:
        kwargs = dict()
        if index_name is not None:
            kwargs["index_name"] = index_name

        response_items = self._query_by_key(key_name=key_name, key_value=key_value,
                                            fields_to_get=["projects"], **kwargs).items
        if len(response_items) > 0:
            projects_data_dict = SafeDict(response_items[0]).get("projects").to_dict(default=None)
            if projects_data_dict is not None:
                projects_database_items_instances: List[ProjectDatabaseItem] = list()
                for project_key_id, project_data in projects_data_dict.items():
                    try:
                        projects_database_items_instances.append(ProjectDatabaseItem(**project_data))
                    except ValidationError as e:
                        print(e)
                return projects_database_items_instances

    def get_all_owned_projects_of_account_by_account_id(self, account_id: str) -> Optional[List[ProjectDatabaseItem]]:
        return self._get_all_owned_projects_of_account(key_name="accountId", key_value=account_id)

    def get_all_owned_projects_of_account_by_account_username(self, account_username: str) -> Optional[List[ProjectDatabaseItem]]:
        return self._get_all_owned_projects_of_account(key_name="username", key_value=account_username, index_name="username")

    def get_infos_of_one_project_build(self, project_resources, build_id: str) -> Optional[AWSBuildInfosBackendModel]:
        from inoft_vocal_engine.cloud_ressources.project_resources import ProjectResources
        project_resources: ProjectResources

        build_infos: Optional[dict] = self._get_value_in_path_target(
            key_name="accountId", key_value=project_resources.project_owner_account_id,
            target_path_elements={"projects": dict, project_resources.account_project_id: dict, "builds": dict, build_id: dict}
        )
        if build_infos is not None:
            try:
                build_infos["buildId"] = build_id
                # We set the buildId in the dict of the build_infos, instead of directly passing the buildId as a
                # kwarg, to avoid issues if for some reasons the buildId kwarg was present in the build_infos dict.
                return AWSBuildInfosBackendModel(**build_infos)
            except ValidationError as e:
                print(e)
        return None

    def set_update_infos_of_one_project_build(self, project_resources, build: AWSBuildInfosBackendModel) -> bool:
        from inoft_vocal_engine.cloud_ressources.project_resources import ProjectResources
        project_resources: ProjectResources

        response = self._add_update_data_element_to_map(
            key_name="accountId", key_value=project_resources.project_owner_account_id,
            object_path_elements={"projects": dict, project_resources.account_project_id: dict, "builds": dict, build.buildId: dict},
            element_values=build.to_database_model().dict()
        )
        if response is not None:
            return True
        return False



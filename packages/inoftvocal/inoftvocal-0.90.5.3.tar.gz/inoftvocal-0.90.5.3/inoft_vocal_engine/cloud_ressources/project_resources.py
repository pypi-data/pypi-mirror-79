from typing import Optional

from inoft_vocal_engine.cloud_ressources.account_resources import AccountResources
from inoft_vocal_engine.cloud_ressources.engine_resources import EngineResources
from inoft_vocal_engine.databases.dynamodb.audio_editor_projects_dynamodb_client import AudioEditorProjectsDynamoDbClient
from inoft_vocal_engine.databases.dynamodb.projects_diagrams_data_dynamodb_client import ProjectsDiagramsDataDynamoDbClient
from inoft_vocal_engine.databases.dynamodb.projects_text_contents_dynamodb_client import \
    ProjectsTextContentsDynamoDbClient, ProjectsTextContentsDynamoDBNewTableClient
from inoft_vocal_engine.databases.dynamodb.team_organization_projects_dynamodb_client import TeamOrganizationProjectsDynamoDbClient
from inoft_vocal_engine.databases.dynamodb.vocal_apps_model_schemas_dynamodb_client import VocalAppsModelSchemasDynamoDBClient
from inoft_vocal_engine.vocal_apps_model_schemas.models import InoftVocalEngineModelSchema


class ProjectResources:
    _project_text_contents_table = None

    _audio_editor_projects_dynamodb_client = None
    _project_text_contents_dynamodb_client = None
    _project_diagrams_data_dynamodb_client = None
    _vocal_apps_model_schemas_dynamodb_client = None
    _team_organization_projects_dynamodb_client = None

    _audio_editor_projects_dynamodb_table_name = "inoft-vocal-engine_accounts-projects-instances_audio-editor-projects-data"
    _project_text_contents_dynamodb_table_name = "inoft-vocal-engine_accounts-projects-instances_text-contents-data"
    _project_diagrams_data_dynamodb_table_name = "inoft-vocal-engine_accounts-projects-instances_diagrams-nodes-data"
    _vocal_apps_model_schemas_dynamodb_table_name = "inoft-vocal-engine_accounts-projects_vocal-apps-model-schemas"
    _team_organization_projects_dynamodb_table_name = "inoft-vocal-engine_accounts-projects-instances_team-organization-projects-data"

    def __init__(self, engine_resources: EngineResources, account_resources: AccountResources,
                 project_url: str, project_owner_account_username: str, project_owner_account_id: str,
                 account_project_id: Optional[str] = None):

        self.engine_resources = engine_resources
        self.account_resources = account_resources
        self.project_url = project_url
        self.project_owner_account_username = project_owner_account_username
        self.project_owner_account_id = project_owner_account_id
        self._account_project_id = account_project_id
        # We have the possibility to set the account_project_id from an argument, because in the
        # auth_workflow, we need to get the account_project_id before we create the ProjectResources
        # instance, because the account_project_id is used in the permissions format.

    @property
    def account_project_id(self) -> str:
        if self._account_project_id is None:
            self._account_project_id = self.engine_resources.accounts_data_dynamodb_client.get_account_project_id_by_project_url(
                account_username=self.account_resources.account_username, project_url=self.project_url
            )
        return self._account_project_id

    """
    @property
    def _project_text_contents_table(self) -> StructNoSQL.BaseTable:
        if self._project_text_contents_table is None:
            self._project_text_contents_table = ProjectsTextContentsDynamoDBNewTableClient(
                table_name=self._project_text_contents_dynamodb_table_name, region_name="eu-west-2"
            )
        return self._audio_editor_projects_dynamodb_client
    """

    @property
    def audio_editor_projects_dynamodb_client(self) -> AudioEditorProjectsDynamoDbClient:
        if self._audio_editor_projects_dynamodb_client is None:
            self._audio_editor_projects_dynamodb_client = AudioEditorProjectsDynamoDbClient(
                table_name=self._audio_editor_projects_dynamodb_table_name, region_name="eu-west-2"
            )
        return self._audio_editor_projects_dynamodb_client

    @property
    def project_text_contents_dynamodb_client(self) -> ProjectsTextContentsDynamoDbClient:
        if self._project_text_contents_dynamodb_client is None:
            self._project_text_contents_dynamodb_client = ProjectsTextContentsDynamoDbClient(
                table_name=self._project_text_contents_dynamodb_table_name, region_name="eu-west-2"
            )
        return self._project_text_contents_dynamodb_client

    @property
    def project_diagrams_data_dynamodb_client(self) -> ProjectsDiagramsDataDynamoDbClient:
        if self._project_diagrams_data_dynamodb_client is None:
            self._project_diagrams_data_dynamodb_client = ProjectsDiagramsDataDynamoDbClient(
                table_name=self._project_diagrams_data_dynamodb_table_name, region_name="eu-west-2"
            )
        return self._project_diagrams_data_dynamodb_client

    @property
    def vocal_apps_model_schemas_dynamodb_client(self) -> VocalAppsModelSchemasDynamoDBClient:
        if self._vocal_apps_model_schemas_dynamodb_client is None:
            self._vocal_apps_model_schemas_dynamodb_client = VocalAppsModelSchemasDynamoDBClient(
                table_name=self._vocal_apps_model_schemas_dynamodb_table_name, region_name="eu-west-2"
            )
        return self._vocal_apps_model_schemas_dynamodb_client

    @property
    def team_organization_projects_dynamodb_client(self) -> TeamOrganizationProjectsDynamoDbClient:
        if self._team_organization_projects_dynamodb_client is None:
            self._team_organization_projects_dynamodb_client = TeamOrganizationProjectsDynamoDbClient(
                table_name=self._team_organization_projects_dynamodb_table_name, region_name="eu-west-2"
            )
        return self._team_organization_projects_dynamodb_client

    def required_template_kwargs(self) -> dict:
        return {
            "project_owner_account_username": self.project_owner_account_username,
            "project_url": self.project_url
        }

    def deploy_lambda(self):
        from inoft_vocal_engine.cloud_providers.aws.deploy import DeployHandler
        from inoft_vocal_engine.utils.paths import get_inoft_vocal_engine_root_path
        DeployHandler().deploy(lambda_files_root_folderpath=get_inoft_vocal_engine_root_path(), stage_name="prod",
                               bucket_name="inoft-vocal-engine-web-test", bucket_region_name="eu-west-3",
                               lambda_name="inoft-vocal-engine-web-interface",
                               lambda_handler="inoft_vocal_engine.web_interface.app.lambda_handler", runtime="python3.7")

    def deploy_project(self):
        from inoft_vocal_engine.cloud_providers.aws.deploy import DeployHandler
        from inoft_vocal_engine.utils.paths import get_inoft_vocal_engine_root_path
        DeployHandler().deploy(lambda_files_root_folderpath=get_inoft_vocal_engine_root_path(), stage_name="prod",
                               bucket_name="inoft-vocal-engine-web-test", bucket_region_name="eu-west-3",
                               lambda_name="inoft-vocal-engine-web-interface",
                               lambda_handler="inoft_vocal_engine.web_interface.app.lambda_handler", runtime="python3.7")


if __name__ == "__main__":
    engine_resources = EngineResources()
    account_resources = AccountResources(engine_resources=engine_resources)
    project_resources = ProjectResources(engine_resources=engine_resources, account_resources=account_resources,
                                         project_url="anvers1944", project_owner_account_username="robinsonlabourdette",
                                         project_owner_account_id="b1fe5939-032b-462d-92e0-a942cd445096")
    project_resources.deploy_lambda()
    # print(resources.project_diagrams_data_dynamodb_client.query_nodes_by_accountProjectId(accountProjectId="5aedb52e-3431-42dc-bf0b-ccd2844d2607"))
    """print(resources.vocal_apps_model_schemas_dynamodb_client.set_update_one_intent(
        accountProjectId=resources.account_project_id,
        intent_model=InoftVocalEngineModelSchema.IntentModel(name="test", samples=["j'aime les test", "yolo"])))"""
    """print(resources.vocal_apps_model_schemas_dynamodb_client.put_model_schema(
        account_project_id=resources.account_project_id,
        model_schema=InoftVocalEngineModelSchema(
        invocationName="test", LanguageModel="fr-FR",
        alexaSpecific={
            "modelConfiguration": {
                "fallbackIntentSensitivity": {
                    "level": "LOW"
                }
            }
        }
    )))"""

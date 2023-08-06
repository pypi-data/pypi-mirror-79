from flask import Blueprint, render_template, request, jsonify
from inoft_vocal_engine.cloud_ressources.account_resources import AccountResources
from inoft_vocal_engine.cloud_ressources.engine_resources import EngineResources
from inoft_vocal_engine.cloud_ressources.project_resources import ProjectResources
from inoft_vocal_engine.web_interface.auth.backend import auth_workflow


control_panel_blueprint = Blueprint("control-panel", __name__, template_folder="templates")
audio_editor_read = "{project_name}:audio-editor:read"


@control_panel_blueprint.route("/<account_username>/control-panel")
def control_panel(account_username: str):
    return auth_workflow(
        account_username=account_username, project_url=None,
        required_permissions=[],
        success_handler=_control_panel, to_template=True
    )

def _control_panel(engine_resources: EngineResources, account_resources: AccountResources, project_resources=None):

    projects = engine_resources.accounts_data_dynamodb_client.get_all_owned_projects_of_account_by_account_username(
        account_username="robinsonlabourdette"
    )
    # todo: fix this fox control panel
    return render_template("control-panel/index.html", account_username="robinsonlabourdette", projects=projects)


@control_panel_blueprint.route("/<account_username>/projects/create", methods=["POST"])
def create_project(account_username: str):
    # todo: add required_permissions
    return auth_workflow(
        account_username=account_username, project_url=None,
        required_permissions=[],
        success_handler=_create_project, to_json=True
    )

def _create_project(engine_resources: EngineResources, account_resources: AccountResources, project_resources=None):
    try:
        from inoft_vocal_engine.models.projects.backend_received_project_data import BackendReceivedProjectData
        project_data = BackendReceivedProjectData(**request.get_json())

        from inoft_vocal_engine.databases.dynamodb.accounts_data_dynamodb_client import ProjectDatabaseItem
        project_database_item = ProjectDatabaseItem(**project_data.dict())

        success = engine_resources.accounts_data_dynamodb_client.add_project_to_account(
            account_id=account_resources.account_id, project_item=project_database_item
        )
        project_complete_url = f"/{account_resources.account_username}/{project_database_item.projectPrimaryUrl}/contents"
        return jsonify(success=success, redirect=project_complete_url)
    except Exception as e:
        print(e)
    return jsonify(success=False)

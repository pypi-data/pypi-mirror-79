import json
from flask import Blueprint, render_template, Response, request, jsonify

from inoft_vocal_engine.cloud_ressources.account_resources import AccountResources
from inoft_vocal_engine.cloud_ressources.engine_resources import EngineResources
from inoft_vocal_engine.cloud_ressources.project_resources import ProjectResources
from inoft_vocal_engine.web_interface.auth.backend import auth_workflow
from inoft_vocal_engine.web_interface.static.ui import SIDEBAR_BUTTONS
from inoft_vocal_engine.web_interface.templates.topbar import topbar_ui

organization_blueprint = Blueprint("organization", __name__, template_folder="templates")

@organization_blueprint.route("/<account_username>/<project_url>/organization")
def organization(account_username: str, project_url: str):
    # todo: add required_permissions
    return auth_workflow(
        account_username=account_username, project_url=project_url,
        required_permissions=[],
        success_handler=_organization, to_template=True
    )

def _organization(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    project_data, request_success = project_resources.team_organization_projects_dynamodb_client.get_project_data_by_account_project_id(
        account_project_id=project_resources.account_project_id
    )
    print(f"project_data = {project_data['M']}")  # todo: fix this shitty way of handling the project data retrieving
    return render_template("team-organization/gantt.html",
                           account_username=account_resources.account_username, project_url=project_resources.project_url,
                           resumed_project_data=json.dumps(project_data['M']), sidebar_buttons=SIDEBAR_BUTTONS,
                           topbar_buttons=topbar_ui.render(
                               account_username=account_resources.account_username,
                               project_url=project_resources.project_url,
                               active_button_id=topbar_ui.ID_ORGANIZATION
                           ))

@organization_blueprint.route("/<account_username>/<project_url>/organization/save", methods=["POST"])
def organization_save(account_username: str, project_url: str):
    # todo: add required_permissions
    return auth_workflow(
        account_username=account_username, project_url=project_url,
        required_permissions=[],
        success_handler=_organization_save, to_json=True
    )

def _organization_save(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    request_json_data = request.get_json()
    print(request_json_data)
    project_resources.team_organization_projects_dynamodb_client.save_project_data(
        account_project_id=project_resources.account_project_id, project_data=request_json_data)

    return jsonify({"success": True})

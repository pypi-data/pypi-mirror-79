from typing import Optional

from flask import Blueprint, render_template, request, jsonify
from pydantic import ValidationError

from inoft_vocal_engine.cloud_ressources.account_resources import AccountResources
from inoft_vocal_engine.cloud_ressources.engine_resources import EngineResources
from inoft_vocal_engine.cloud_ressources.project_resources import ProjectResources
from inoft_vocal_engine.smapi_clients.smapi_base_client import SmapiBaseClient
from inoft_vocal_engine.web_interface.auth.backend import auth_workflow

builds_blueprint = Blueprint("builds", __name__, template_folder="templates")

@builds_blueprint.route("/<account_username>/<project_url>/builds")
def builds(account_username: str, project_url: str):
    return auth_workflow(
        account_username=account_username, project_url=project_url,
        required_permissions=[],
        success_handler=_builds, to_template=True,
    )

def _builds(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    from inoft_vocal_engine.cloud_providers.aws.deploy import DeployHandler
    build_data = DeployHandler().deploy(engine_resources=engine_resources, project_resources=project_resources, lambda_handler="diagrams_0.py")
    success = engine_resources.accounts_data_dynamodb_client.set_update_infos_of_one_project_build(
        project_resources=project_resources, build=build_data
    )

    return render_template(
        "deployment/deployment.html",
        **project_resources.required_template_kwargs()
    )


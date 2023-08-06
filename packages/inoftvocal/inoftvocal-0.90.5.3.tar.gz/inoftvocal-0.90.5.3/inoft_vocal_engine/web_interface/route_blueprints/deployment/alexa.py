from flask import Blueprint

from inoft_vocal_engine.cloud_ressources.account_resources import AccountResources
from inoft_vocal_engine.cloud_ressources.engine_resources import EngineResources
from inoft_vocal_engine.cloud_ressources.project_resources import ProjectResources
from inoft_vocal_engine.web_interface.auth.backend import auth_workflow

alexa_deployment_blueprint = Blueprint("auth", __name__, template_folder="templates")

"""
@alexa_deployment_blueprint.route("/<account_username>/<project_url>/deployment/alexa/skill-manifest/set", methods=["POST"])
def set_alexa_skill_manifest(account_username: str, project_url: str):
    return auth_workflow(
        account_username=account_username, project_url=project_url,
        required_permissions=[],
        success_handler=_set_alexa_skill_manifest, to_json=True,
    )

def _set_alexa_skill_manifest(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    try:
        say_text_action = SayTextAction(**request.get_json())
        print(say_text_action)
    return {"success": True}
"""

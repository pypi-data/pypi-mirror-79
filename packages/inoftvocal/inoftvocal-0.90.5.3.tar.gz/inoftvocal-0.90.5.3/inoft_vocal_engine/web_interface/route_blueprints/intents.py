import json

from flask import Blueprint, render_template, request, Response, jsonify
from pydantic import ValidationError
from typing import List

from inoft_vocal_engine.cloud_ressources.account_resources import AccountResources
from inoft_vocal_engine.cloud_ressources.engine_resources import EngineResources
from inoft_vocal_engine.cloud_ressources.project_resources import ProjectResources
from inoft_vocal_engine.safe_dict import SafeDict
from inoft_vocal_engine.web_interface.auth.backend import auth_workflow

intents_blueprint = Blueprint("intents", __name__, template_folder="templates")


@intents_blueprint.route("/<account_username>/<project_url>/intents", methods=["GET"])
def intents(account_username: str, project_url: str):
    # todo: add required_permissions
    return auth_workflow(
        account_username=account_username, required_permissions=[],
        success_handler=_intents, to_template=True,
        project_url=project_url
    )

def _intents(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    intents_instances_list = project_resources.vocal_apps_model_schemas_dynamodb_client.get_all_intents_instances_by_account_project_id(
        account_project_id=project_resources.account_project_id
    )
    return render_template("intents/intents_index.html", intents=intents_instances_list,
                           **project_resources.required_template_kwargs())

@intents_blueprint.route("/<account_username>/<project_url>/intents/get-all", methods=["GET"])
def get_all_intents(account_username: str, project_url: str):
    # todo: add required_permissions
    return auth_workflow(
        account_username=account_username, required_permissions=[],
        success_handler=_get_all_intents, to_json=True,
        project_url=project_url
    )

def _get_all_intents(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    intents_instances_list = project_resources.vocal_apps_model_schemas_dynamodb_client.get_all_intents_dicts_by_account_project_id(
        account_project_id=project_resources.account_project_id
    )
    return jsonify(success=True, intents=intents_instances_list)

@intents_blueprint.route("/<account_username>/<project_url>/intents/set/one", methods=["POST"])
def set_one_intent(account_username: str, project_url: str):
    # todo: add required_permissions
    return auth_workflow(
        account_username=account_username, required_permissions=[],
        success_handler=_set_one_intent, to_json=True,
        project_url=project_url
    )

def _set_one_intent(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    from inoft_vocal_engine.vocal_apps_model_schemas.models import InoftVocalEngineModelSchema
    try:
        intent_model = InoftVocalEngineModelSchema.IntentModel(**request.get_json())
        response = project_resources.vocal_apps_model_schemas_dynamodb_client.set_update_one_intent(
            accountProjectId=project_resources.project_owner_account_id, intent_model=intent_model
        )
    except ValidationError as e:
        print(f"Error while validating an intent model data : {e}")
        return jsonify(success=False)

@intents_blueprint.route("/<account_username>/<project_url>/intents/set/multiple", methods=["POST"])
def set_multiple_intents(account_username: str, project_url: str):
    # todo: add required_permissions
    return auth_workflow(
        account_username=account_username, required_permissions=[],
        success_handler=_set_multiple_intents, to_json=True,
        project_url=project_url
    )

def _set_multiple_intents(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    from inoft_vocal_engine.vocal_apps_model_schemas.models import InoftVocalEngineModelSchema
    updated_intents_ids: List[str] = list()
    # Instead of returning an error if any intent has a ValidationError or a database error, we keep a list of the ids
    # of all the intents that have been successfully updated, which we will returned to the client backend, so that it
    # will be able to know which intents have been updated and do not need to be send again, and which intents have had
    # an error, that need to be send back the next time the intents are saved. This approach, allow that if one of the
    # the intent send by the client has an error, it will not block all the potential others intents send by the client.
    intents_data_list = SafeDict(request.get_json()).get("intents").to_list(default=None)
    if intents_data_list is not None:
        for intent_data in intents_data_list:
            try:
                intent_model = InoftVocalEngineModelSchema.IntentModel(**intent_data)
                response = project_resources.vocal_apps_model_schemas_dynamodb_client.set_update_one_intent(
                    accountProjectId=project_resources.account_project_id, intent_model=intent_model
                )
                if response is not None:
                    # If the response is None, there has been an error.
                    updated_intents_ids.append(intent_model.intentId)
            except ValidationError as e:
                print(f"Error while validating an intent model data : {e}")

    return jsonify(updatedIntentsIds=updated_intents_ids)





from typing import Optional

from flask import Blueprint, render_template, request, jsonify
from pydantic import ValidationError

from inoft_vocal_engine.cloud_ressources.account_resources import AccountResources
from inoft_vocal_engine.cloud_ressources.engine_resources import EngineResources
from inoft_vocal_engine.cloud_ressources.project_resources import ProjectResources
from inoft_vocal_engine.smapi_clients.smapi_base_client import SmapiBaseClient
from inoft_vocal_engine.web_interface.auth.backend import auth_workflow
from inoft_vocal_engine.web_interface.route_blueprints.deployment.models import ApplicationManifestUpdateRequestData, \
    ApplicationManifestGetRequestData, switch_key_type_to_data_models

deployment_blueprint = Blueprint("deployment", __name__, template_folder="templates")

@deployment_blueprint.route("/<account_username>/<project_url>/deployment")
def deployment(account_username: str, project_url: str):
    return auth_workflow(
        account_username=account_username, project_url=project_url,
        required_permissions=[],
        success_handler=_deployment, to_template=True,
    )

def _deployment(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    return render_template(
        "deployment/deployment.html",
        **project_resources.required_template_kwargs()
    )


@deployment_blueprint.route("/<account_username>/<project_url>/publishing/get", methods=["POST"])
def get_publishing_infos(account_username: str, project_url: str):
    return auth_workflow(
        account_username=account_username, project_url=project_url,
        required_permissions=[],
        success_handler=_get_publishing_infos, to_json=True,
    )

def _get_publishing_infos(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    try:
        request_data = ApplicationManifestGetRequestData(**request.get_json())
        validators_class_types = switch_key_type_to_data_models.get(request_data.typeKeyName, None)
        if validators_class_types is not None:
            validator_class_instance = validators_class_types.base(**request_data.data)

            response_item_dict: Optional[dict] = project_resources.vocal_apps_model_schemas_dynamodb_client.get_item_in_path_target(
                account_project_id=project_resources.account_project_id,
                target_path_elements=validator_class_instance.database_path,
            )
            if response_item_dict is not None:
                sender_validator_class_instance = validators_class_types.sender(**response_item_dict)
                return jsonify({"success": True, "data": sender_validator_class_instance.json()})
    except ValidationError as e:
        print(e)
    return jsonify({"success": False})

@deployment_blueprint.route("/<account_username>/<project_url>/publishing/update", methods=["POST"])
def update_publishing_infos(account_username: str, project_url: str):
    return auth_workflow(
        account_username=account_username, project_url=project_url,
        required_permissions=[],
        success_handler=_update_publishing_infos, to_json=True,
    )

def _update_publishing_infos(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    try:
        request_data = ApplicationManifestUpdateRequestData(**request.get_json())
        validators_class_types = switch_key_type_to_data_models.get(request_data.typeKeyName, None)
        if validators_class_types is not None:
            validator_class_instance = validators_class_types.update(**request_data.data)

            response = project_resources.vocal_apps_model_schemas_dynamodb_client.update_value_with_path_target(
                account_project_id=project_resources.account_project_id,
                object_path_elements=validator_class_instance.database_path,
                value=validator_class_instance.export()
            )
            return jsonify({"success": True})
    except ValidationError as e:
        print(e)
    return jsonify({"success": False})


"""

        refresh_token = "Atzr|IwEBIJPMVNBwbBGY2hum-1Q0ldBPx4wXyFiPr38X9F1Y4FgPYjHvTLK5UlsG5z4kXZlMZHIYGDQLtFFw7saqZ4ZEaRalmjLfdR62uBXe_PupGVrrsX3721TZrSG68Om7VvBCFqJS3BHM_AG5b9VFJkDIkmO5wz45vo9S-6JR1I2KLB12N_vGSKZ5SfIma1PSHjfeAeQgWBQfIa19KE0xBw8t9U0fyGaM-JvwxoLulf1k265hWUDDj3Uuve5CbUlU41NHtFYZXbVrj76vEGIw7-HZBoKU0ZA1-_oscarmnZ5b5ENFFIuKt-bGbQJw5ycgT0Gm0Ja3sxGI7EpakcGBIOECOl0Am4QZBCBRtRENvHVHKtjhT2PeZEZh9Re_DB4nRnnpJOXXXiwajfNdcvtSPHP9nOXtg64iaALnZBeZzzzhcVEXsqQh9TEwO1Y6nOGFMtDm-zOFulGjDwvz_ySLmA5qGbjz9o4p_-A5DEXG2zIgezPT0Z_SyqsiVq7GJ3ixAydyG_4R7nSGEo63_tt34Ffuq4-eSV605Rt7nEHUivm5M9QFOUargug98MlZJala-z_x1u5ETJAZpVhxkXfl4b-XMbqA1YkW2wfO9IkJf_P2UzX2rY1TPz9nGn_DUiVSeGucePo"
        # todo: make refresh token dynamic (store the refresh token of an user in the database after he logged with
        #  amazon, and if the token is not found, or was not working, prompt the user to login with amazon)
        smapi_client = SmapiBaseClient(refresh_token=refresh_token)
        smapi_client.create_skill(vendor_id=smapi_client.get_vendors_of_account()[0].id,
                                  skill_manifest=publishing_infos.to_alexa_manifest())
        # todo: instead of getting the first vendor of the account, get the main vendor of the account
"""
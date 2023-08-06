from flask import Blueprint, render_template, jsonify, request
from typing import List

from inoft_vocal_engine.cloud_ressources.account_resources import AccountResources
from inoft_vocal_engine.cloud_ressources.engine_resources import EngineResources
from inoft_vocal_engine.cloud_ressources.project_resources import ProjectResources
from inoft_vocal_engine.web_interface.auth.backend import auth_workflow
from inoft_vocal_engine.web_interface.static.ui import SIDEBAR_BUTTONS
from inoft_vocal_engine.web_interface.templates.topbar import topbar_ui

code_editor_blueprint = Blueprint("code-editor", __name__, template_folder="templates")

@code_editor_blueprint.route("/<account_username>/<project_url>/code-editor")
def code_editor(account_username: str, project_url: str):
    return auth_workflow(
        account_username=account_username, project_url=project_url,
        required_permissions=[],
        success_handler=_code_editor, to_template=True,
    )

def _code_editor(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    generated_files = _generate_application_code(project_resources=project_resources)

    # from inoft_vocal_engine.cloud_providers.aws.generated_code_s3_client import GeneratedCodeS3Client
    # app_code = GeneratedCodeS3Client().get_app_code()

    return render_template(
        "code-editor/index.html", app_code=generated_files[0],
        sidebar_buttons=SIDEBAR_BUTTONS,
        topbar_buttons=topbar_ui.render(
            account_username=project_resources.project_owner_account_username,
            project_url=project_resources.project_url,
            active_button_id=topbar_ui.ID_ORGANIZATION
        ),
        **project_resources.required_template_kwargs()
    )

def _generate_application_code(project_resources: ProjectResources) -> List[str]:
    from inoft_vocal_engine.code_generation.generator import GeneratorCore
    code_generated_files = GeneratorCore(project_resources=project_resources).generate()

    from inoft_vocal_engine.cloud_providers.aws.generated_code_s3_client import GeneratedCodeS3Client
    s3_client = GeneratedCodeS3Client()

    # todo: make it possible to have custom filename, instead of just diagrams_{i}
    for i, file in enumerate(code_generated_files):
        s3_client.upload_app_code(project_resources=project_resources, app_code=file, key_filename=f"diagrams.py")

    return code_generated_files

"""
@audio_editor_blueprint.route("/audio-editor/<account_project_id>/save", methods=["POST"])
def audio_editor_save(account_project_id: str):
    print(f"Saving data for project {account_project_id}")

    request_json_data = request.get_json()
    if request_json_data is not None:
        request_success = project_resources.audio_editor_projects_dynamodb_client.save_project_data(account_project_id=account_project_id,
                                                                                                    project_data=request_json_data)
    else:
        request_success = False

    return jsonify({"success": request_success})
"""


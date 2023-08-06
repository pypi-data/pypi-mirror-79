from flask import Blueprint, render_template, jsonify, request

from inoft_vocal_engine.cloud_ressources.account_resources import AccountResources
from inoft_vocal_engine.cloud_ressources.engine_resources import EngineResources
from inoft_vocal_engine.cloud_ressources.project_resources import ProjectResources
from inoft_vocal_engine.web_interface.auth.backend import auth_workflow
from inoft_vocal_engine.web_interface.route_blueprints.audio_project import AudioProject
from inoft_vocal_engine.web_interface.static.ui import SIDEBAR_BUTTONS
from inoft_vocal_engine.web_interface.templates.topbar import topbar_ui

audio_editor_blueprint = Blueprint("audio-editor", __name__, template_folder="templates")

dice = {
    'projectId': True,
    'collections': {
        'tracks': {
            'models': [{
                'attributes': {
                    'file': {
                        'name': 'jean sablon - alexa.mp3',
                        'webkitRelativePath': '',
                        'lastModified': 1591264478848.0,
                        'size': 1007568.0,
                        'type': 'audio/mpeg'
                    },
                    'color': '#00a0b0',
                    'length': 1920.0,
                    'name': 'Track 1',
                    'solo': False,
                    'buffer': {
                        'duration': 167.71,
                        'length': 7396188.0,
                        'sampleRate': 44100.0,
                        'numberOfChannels': 2.0
                    },
                    'pan': 0,
                    'muted': False,
                    'gain': 1.0,
                }
            }]
        },
    }
}

if __name__ == "__main__":
    audio_project = AudioProject(**dice)
    audio_project.add_track()
    print(audio_project)


@audio_editor_blueprint.route("/audio-editor-v2")
def audio_editor_v2():
    return render_template("audio-editor-v2/index.html")

@audio_editor_blueprint.route("/<account_username>/<project_url>/audio-editor")
def audio_editor(account_username: str, project_url: str):
    return auth_workflow(
        account_username=account_username, project_url=project_url,
        required_permissions=[],
        success_handler=_audio_editor, to_template=True,
    )


def _audio_editor(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    # audio_project_data, audio_request_success = project_resources.audio_editor_projects_dynamodb_client.get_project_data_by_account_project_id(account_project_id=project_resources.account_project_id)
    # text_project_data, text_request_success = project_resources.project_text_contents_dynamodb_client.get_by_id(account_project_id=project_resources.account_project_id)
    # audio_project = NestedObjectToDict.dict_to_typed_class(class_type=AudioProject, data_dict=audio_project_data)
    # print(f"audio_project = {audio_project}")
    # print(f"audio_project_data = {audio_project_data}\n& text_project_data = {text_project_data}")

    static_data = {'Collections': {'Tracks': {'models': [{'attributes': {
        'buffer': {'duration': 167.714, 'length': 8050272, 'numberOfChannels': 2, 'sampleRate': 48000},
        'color': '#00a0b0', 'file': {'lastModified': 1591264478848, 'name': 'jean sablon - alexa.mp3', 'size': 1007568,
                                     'type': 'audio/mpeg', 'webkitRelativePath': ''}, 'gain': 1, 'length': 1920,
        'muted': False, 'name': 'Track 1', 'pan': 0.5, 'solo': False}}]}}}

    return render_template("audio-editor/index.html", project_data=static_data,
                           sidebar_buttons=SIDEBAR_BUTTONS,
                           topbar_buttons=topbar_ui.render(
                               account_username=project_resources.project_owner_account_username,
                               project_url=project_resources.project_url,
                               active_button_id=topbar_ui.ID_ORGANIZATION
                           ), **project_resources.required_template_kwargs())

@audio_editor_blueprint.route("/<account_username>/<project_url>/audio-editor/save", methods=["POST"])
def audio_editor_save(account_username: str, project_url: str):
    project_resources = ProjectResources(engine_resources=EngineResources(), account_username=account_username, project_url=project_url)
    print(f"Saving data for project {project_url}")

    request_json_data = request.get_json()
    if request_json_data is not None:
        request_success = project_resources.audio_editor_projects_dynamodb_client.save_project_data(
            account_project_id=project_resources.account_project_id, project_data=request_json_data)
    else:
        request_success = False

    return jsonify({"success": request_success})

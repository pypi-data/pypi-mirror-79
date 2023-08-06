from flask import Blueprint, render_template, Response, request, jsonify

from inoft_vocal_engine.cloud_ressources.account_resources import AccountResources
from inoft_vocal_engine.cloud_ressources.engine_resources import EngineResources
from inoft_vocal_engine.cloud_ressources.project_resources import ProjectResources
from inoft_vocal_engine.safe_dict import SafeDict
from inoft_vocal_engine.web_interface.auth.backend import auth_workflow
from inoft_vocal_engine.web_interface.templates.topbar import topbar_ui
from inoft_vocal_engine.web_interface.templates.local_toolbars import ui as local_toolbars_ui

contents_blueprint = Blueprint("contents", __name__, template_folder="templates")

# todo: make it so that when we update the content list, we also reset up the text fields
#  (because currently, they are not re-setup when the html is being replaced)
# todo: make the search capital case insensitive
# todo: fix issue where the characterNames list in the database will only be set when importing from botpress,
#  but not set when updating or adding a new content (even if currently, its only possible to update, not to add)

@contents_blueprint.route("/<account_username>/<project_url>/contents")
def contents(account_username: str, project_url: str):
    # todo: add required_permissions
    return auth_workflow(
        account_username=account_username, project_url=project_url,
        required_permissions=[],
        success_handler=_contents, to_template=True
    )

def _contents(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    from inoft_vocal_engine.web_interface.static.ui import SIDEBAR_BUTTONS
    return render_template("index.html", account_username=account_resources.account_username,
                           project_url=project_resources.project_url,
                           list_content=_get_latest_updated_contents(project_resources=project_resources)["html"],
                           sidebar_buttons=SIDEBAR_BUTTONS,
                           topbar_buttons=topbar_ui.render(
                               account_username=account_resources.account_username,
                               project_url=project_resources.project_url,
                               active_button_id=topbar_ui.ID_CONTENT
                           ),
                           local_topbar_buttons=local_toolbars_ui.CONTENT_LOCAL_TOOLBAR_BUTTONS)


@contents_blueprint.route("/<account_username>/<project_url>/contents/upload", methods=["POST"])
def upload_post_contents(account_username: str, project_url: str):
    project_resources = ProjectResources(engine_resources=EngineResources(), account_username=account_username, project_url=project_url)

    request_json_data = SafeDict(request.get_json())
    content_elements = request_json_data.get("contentElements").to_list(default=None)
    if content_elements is not None:
        from inoft_vocal_engine.import_integrations.botpress.content_elements import put_new_botpress_contents_from_list
        put_new_botpress_contents_from_list(contents_list=content_elements, project_resources=project_resources)

    return Response(status=200)

@contents_blueprint.route("/<account_username>/<project_url>/contents/update/<element_id>", methods=["POST"])
def update_text_content(account_username: str, project_url: str, element_id: str):
    project_resources = ProjectResources(engine_resources=EngineResources(), account_username=account_username, project_url=project_url)

    request_json_data = SafeDict(request.get_json())
    print(request_json_data)
    return Response(status=200)

    dialogue_line_index = request_json_data.get("dialogueLineIndex").to_int(default=None)
    element_text = request_json_data.get("text").to_str(default=None)

    project_resources.project_text_contents_dynamodb_client.update_content_element(
        element_id=element_id, dialogue_line_index=dialogue_line_index, element_text=element_text)

    return Response(status=200)

@contents_blueprint.route("/<account_username>/<project_url>/contents/latest-updated", methods=["GET"])
def get_latest_updated_contents(account_username: str, project_url: str):
    project_resources = ProjectResources(engine_resources=EngineResources(), account_username=account_username, project_url=project_url)
    return _get_latest_updated_contents(project_resources=project_resources)

def _get_latest_updated_contents(project_resources: ProjectResources):
    content_items = project_resources.project_text_contents_dynamodb_client.get_latest_updated(num_latest_items=30).items
    # todo: make latest contents customizable in the backend and in the frontend
    return {"html": render_template("list_content_elements/list.html", elements=content_items)}

@contents_blueprint.route("/<account_username>/<project_url>/contents/characterName", methods=["GET"])
def get_contents_by_character_name(account_username: str, project_url: str):
    project_resources = ProjectResources(engine_resources=EngineResources(), account_username=account_username, project_url=project_url)

    character_name = request.args.get('inputValue', default=None, type=str)
    if character_name is not None:
        database_response = project_resources.project_text_contents_dynamodb_client.get_by_character_name(character_name=character_name)
        if database_response.items is not None and len(database_response.items) > 0:
            return jsonify({"html": render_template("list_content_elements/list.html", elements=database_response.items)})

    return jsonify({"html": "<p>Aucun résultats trouvés</p>"})

@contents_blueprint.route("/<account_username>/<project_url>/contents/text", methods=["GET"])
def get_contents_by_text_search(account_username: str, project_url: str):
    project_resources = ProjectResources(engine_resources=EngineResources(), account_username=account_username, project_url=project_url)

    text_to_search = request.args.get('inputValue', default=None, type=str)
    if text_to_search is not None:
        database_response = project_resources.project_text_contents_dynamodb_client.get_by_text_search(
            text_to_search=text_to_search, section_instance_id=12
        )
        # todo: make non-static
        if database_response.items is not None and len(database_response.items) > 0:
            return jsonify({"html": render_template("list_content_elements/list.html", elements=database_response.items)})

    # todo: replace standard text by a template to inform that no results have been found
    return jsonify({"html": "<p>Aucun résultats trouvés</p>"})


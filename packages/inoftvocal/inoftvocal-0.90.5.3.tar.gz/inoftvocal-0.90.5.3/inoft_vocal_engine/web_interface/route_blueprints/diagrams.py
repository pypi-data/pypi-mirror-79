import json
from flask import Blueprint, render_template, request, Response, jsonify
from pydantic import ValidationError
from typing import List

from inoft_vocal_engine.cloud_ressources.account_resources import AccountResources
from inoft_vocal_engine.cloud_ressources.engine_resources import EngineResources
from inoft_vocal_engine.cloud_ressources.project_resources import ProjectResources
from inoft_vocal_engine.databases.dynamodb.utils import remove_null_elements_from_dict
from inoft_vocal_engine.safe_dict import SafeDict
from inoft_vocal_engine.web_interface.auth.backend import auth_workflow

diagrams_blueprint = Blueprint("diagrams", __name__, template_folder="templates")

@diagrams_blueprint.route("/<account_username>/<project_url>/diagrams")
def diagrams(account_username: str, project_url: str):
    from inoft_vocal_engine.permissions.diagrams import project_diagrams_nodes_read_all
    return auth_workflow(
        account_username=account_username, project_url=project_url,
        required_permissions=[project_diagrams_nodes_read_all],
        success_handler=_diagrams, to_template=True,
    )

def _diagrams(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    response = project_resources.project_diagrams_data_dynamodb_client.query_nodes_by_project_id(
        project_id=project_resources.account_project_id
    )

    from inoft_vocal_engine.import_integrations.botpress.engine_models import NodeDatabaseItem
    nodes_data_dicts: List[dict] = list()
    for item in response.items:
        if isinstance(item, dict):
            current_node_database_item = NodeDatabaseItem(**item)
            nodes_data_dicts.append(current_node_database_item.to_processed_node_element().dict())

    return render_template("diagrams/index.html", nodes_data=json.dumps(nodes_data_dicts),
                           **project_resources.required_template_kwargs())

# todo: centralize the imports and import the bot all at once
@diagrams_blueprint.route("/<account_username>/<project_url>/diagrams/import/botpress/bot", methods=["POST"])
def import_botpress_bot(account_username: str, project_url: str):
    zip_file = request.data
    binary_file_path = 'file.zip'  # Name for new zip file you want to regenerate
    with open(binary_file_path, 'wb') as f:
        f.write(zip_file)
    input()

# todo: rename this function to import/botpress
@diagrams_blueprint.route("/<account_username>/<project_url>/diagrams/upload", methods=["POST"])
def upload_diagrams_data(account_username: str, project_url: str):
    return auth_workflow(
        account_username=account_username, project_url=project_url,
        required_permissions=[],
        success_handler=_upload_diagrams_data, to_json=True,
    )

def _upload_diagrams_data(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    request_json_data = SafeDict(request.get_json())
    diagram_data = request_json_data.get("diagramData").to_safedict()
    # todo: save the rest of the fields of the diagram data (version, catchAll, startNode, description)
    #  in a separate database, like the accountDiagramsDatabaseClient
    node_elements = diagram_data.get("nodes").to_list(default=None)
    if node_elements is not None:
        from inoft_vocal_engine.import_integrations.botpress.diagrams_data import put_new_botpress_diagrams_data_from_list
        put_new_botpress_diagrams_data_from_list(nodes_list=node_elements,
            projects_diagrams_data_dynamodb_client=project_resources.project_diagrams_data_dynamodb_client)

    generate_code(project_resources=project_resources)
    # todo: create a button on the ui that can generated the code, and create a build system

    return Response(status=200)

perm = "{account_username}:{project_id}:diagrams:nodes:update:all"

# todo: rename this function to import/botpress
@diagrams_blueprint.route("/<account_username>/<project_url>/diagrams/nodes/update", methods=["POST"])
def update_nodes(account_username: str, project_url: str):
    from inoft_vocal_engine.permissions.diagrams import project_diagrams_nodes_update_all
    return auth_workflow(
        account_username=account_username, project_url=project_url,
        required_permissions=[project_diagrams_nodes_update_all],
        success_handler=_update_nodes, to_json=True,
    )

def _update_nodes(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    nodes_data = SafeDict(request.get_json()).get("nodesData").to_list()
    print(nodes_data)

    from inoft_vocal_engine.import_integrations.botpress.engine_models import NodeElementDataReceivedFromUser
    for node in nodes_data:
        try:
            node_element = NodeElementDataReceivedFromUser(**node)
            project_resources.project_diagrams_data_dynamodb_client.update_node(node_element_data=node_element)
        except ValidationError as e:
            print(e)

    return jsonify(success=True)

@diagrams_blueprint.route("/<account_username>/<project_url>/diagrams/nodes/add", methods=["POST"])
def add_nodes(account_username: str, project_url: str):
    # todo: add required_permissions
    return auth_workflow(
        account_username=account_username, project_url=project_url,
        required_permissions=[],
        success_handler=_add_nodes, to_json=True,
    )

def _add_nodes(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    nodes_data = SafeDict(request.get_json()).get("nodesData").to_list()
    print(nodes_data)

    from inoft_vocal_engine.import_integrations.botpress.engine_models import NodeElementDataReceivedFromUser, NodeDatabaseItem
    for node in nodes_data:
        try:
            node_element = NodeElementDataReceivedFromUser(**node)
            node_database_item = NodeDatabaseItem(
                accountId=project_resources.project_owner_account_id,
                accountProjectId=project_resources.account_project_id,
                accountProjectInstanceId="null",
                **remove_null_elements_from_dict(node_element.dict())
            )
            project_resources.project_diagrams_data_dynamodb_client.put_new_node(node_database_item)
        except ValidationError as e:
            print(e)

    return Response(status=200)

@diagrams_blueprint.route("/<account_username>/<project_url>/diagrams/links/add", methods=["POST"])
def add_links(account_username: str, project_url: str):
    # todo: add required_permissions
    return auth_workflow(
        account_username=account_username, project_url=project_url,
        required_permissions=[],
        success_handler=_add_links, to_json=True,
    )

def _add_links(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    links_data = SafeDict(request.get_json()).to_list()

    from inoft_vocal_engine.import_integrations.botpress.engine_models import DatabaseTransitionConditionItem
    for link in links_data:
        try:
            transition_condition = DatabaseTransitionConditionItem(**link)
            project_resources.project_diagrams_data_dynamodb_client.add_update_transition_to_node(
                transition_condition=transition_condition
            )
        except ValidationError as e:
            print(e)

    return jsonify(success=True)



@diagrams_blueprint.route("/<account_username>/<project_url>/diagrams/actions/create/one", methods=["POST"])
def create_one_action(account_username: str, project_url: str):
    # todo: add required_permissions
    return auth_workflow(
        account_username=account_username, project_url=project_url,
        required_permissions=[],
        success_handler=_create_one_action, to_json=True,
    )

def _create_one_action(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    from inoft_vocal_engine.models.actions import SayTextAction
    try:
        # todo: add support for multiple types of actions

        say_text_action = SayTextAction.make_new(text_content_id=None, **request.get_json())
        # Create a new SayTextAction to validate the arguments, and initialize the action id.

        from inoft_vocal_engine.inoft_vocal_markup.deserializer import Deserializer
        inoft_vocal_markup_deserializer = Deserializer(characters_names=["Léo", "Willie", "Menu"])
        # Create a markup deserializer, that will be passed to the ContentDatabaseItem, so that we can get the
        # dialogues lines of the crudeText, which will allow us to get the names of the characters in a dialogue.
        # todo: make creation of deserializer dynamic based on character names stored in a database

        from inoft_vocal_engine.databases.dynamodb.projects_text_contents_dynamodb_client import ContentDatabaseItem
        text_content_item = ContentDatabaseItem.make_new(
            crude_text=say_text_action.loadedTextToSay,
            markup_deserializer=inoft_vocal_markup_deserializer,
            ids_instances_using_content=["say_text_action.instanceId"]
            # todo: add instanceId in the BaseAction class
        )
        project_resources.project_text_contents_dynamodb_client.put_new_content(text_content_item)
        # Once created, put the new content item in the database.

        say_text_action.textContentItemId = text_content_item.elementId
        # Once its done, we cna assign the content item id to the say_text_action. We needed to create the
        # say_text_action element before the text_content_item, in order to access the action instanceId,
        # after the data as been correctly validated by passing it in the SayTextAction class.
        response = project_resources.project_diagrams_data_dynamodb_client.add_update_action_to_node(action_instance=say_text_action)
        # Then, we can simply add the action to the node.

        say_text_action.isNew = False
        # We set the isNew value on False, so that when we return the new object that will be load in the
        # client browser, the action will not be considered as new, and will now be updated instead of created.

        if response is not None:
            return jsonify(success=True, action=say_text_action.dict())
    except ValidationError as e:
        print(e)
    return jsonify(success=False)

@diagrams_blueprint.route("/<account_username>/<project_url>/diagrams/actions/update/one", methods=["POST"])
def update_one_action(account_username: str, project_url: str):
    # todo: add required_permissions
    return auth_workflow(
        account_username=account_username, project_url=project_url,
        required_permissions=[],
        success_handler=_update_one_action, to_json=True,
    )

def _update_one_action(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    from inoft_vocal_engine.models.actions import SayTextAction
    try:
        say_text_action = SayTextAction(**request.get_json())
        print(say_text_action)
        response = project_resources.project_diagrams_data_dynamodb_client.add_update_action_to_node(action_instance=say_text_action)

        # todo: update text element if the action is a SayTextAction

        return jsonify(success=True)
    except ValidationError as e:
        print(e)
        return jsonify(success=False)

@diagrams_blueprint.route("/<account_username>/<project_url>/diagrams/create-new", methods=["POST"])
def create_new_diagram(account_username: str, project_url: str):
    # todo: add required_permissions
    return auth_workflow(
        account_username=account_username, project_url=project_url,
        required_permissions=[],
        success_handler=_create_new_diagram, to_json=True,
    )

def _create_new_diagram(engine_resources: EngineResources, account_resources: AccountResources, project_resources: ProjectResources):
    from inoft_vocal_engine.databases.dynamodb.accounts_data_dynamodb_client import InstanceInfoDatabaseItem
    request_data = SafeDict(request.get_json())

    instance_name = request_data.get("instanceName").to_str(default=None)
    if instance_name is None:
        return jsonify({"success": False})
    else:
        instance_description = request_data.get("instanceDescription").to_str(default=None)
        operation_success = engine_resources.accounts_data_dynamodb_client.add_instance_infos_to_account(
            account_id=project_resources.project_owner_account_id,
            instance_infos_item=InstanceInfoDatabaseItem(
                projectId=project_resources.account_project_id,
                instanceName=instance_name, instanceDescription=instance_description
            )
        )
        return jsonify({"success": operation_success})



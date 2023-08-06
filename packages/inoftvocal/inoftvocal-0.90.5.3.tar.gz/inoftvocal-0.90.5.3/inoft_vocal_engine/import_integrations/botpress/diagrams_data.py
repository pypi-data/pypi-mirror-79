from typing import List, Dict
from inoft_vocal_engine.databases.dynamodb.projects_diagrams_data_dynamodb_client import ProjectsDiagramsDataDynamoDbClient
from inoft_vocal_engine.safe_dict import SafeDict
from inoft_vocal_engine.import_integrations.botpress.engine_models import ProcessedNodeElement, DatabaseTransitionConditionItem


def botpress_diagrams_json_object_to_list_content_elements(list_all_node_elements: list) -> List[ProcessedNodeElement]:
    nodes_names_to_instances: Dict[str, dict] = dict()
    for node_data in list_all_node_elements:
        current_node_name = SafeDict(node_data).get("name").to_str(default=None)
        if current_node_name is not None:
            nodes_names_to_instances[current_node_name] = node_data

    node_elements: List[ProcessedNodeElement] = list()
    for node_data in list_all_node_elements:
        current_node_safedict = SafeDict(node_data)
        current_node_object = ProcessedNodeElement()

        current_node_object.node_id = current_node_safedict.get("id").to_str(default=None)
        current_node_object.node_name = current_node_safedict.get("name").to_str(default=None)
        current_node_object.node_type = current_node_safedict.get("type").to_str(default=None)
        current_node_object.actions = current_node_safedict.get("onEnter").to_list(default=None)
        current_node_object.temp_on_receive = current_node_safedict.get("onReceive").to_list(default=None)

        next_items = current_node_safedict.get("next").to_list(default=None)
        if next_items is not None:
            next_instances: List[DatabaseTransitionConditionItem] = list()
            for next_item in next_items:
                current_next_item_safedict = SafeDict(next_item)
                current_next_item_condition = current_next_item_safedict.get('condition').to_str(default=None)

                current_next_item_target_node_name = current_next_item_safedict.get("node").to_str(default=None)
                if current_next_item_target_node_name in nodes_names_to_instances.keys():
                    current_next_item_target_node_safedict = SafeDict(nodes_names_to_instances[current_next_item_target_node_name])
                    current_next_item_outPortNodeId = current_next_item_target_node_safedict.get("id").to_str(default=None)
                else:
                    current_next_item_outPortNodeId = None

                next_instances.append(DatabaseTransitionConditionItem(condition=current_next_item_condition,
                                                    targetNodeId=current_next_item_outPortNodeId))
            current_node_object.next = next_instances
        node_elements.append(current_node_object)
    return node_elements

def botpress_diagrams_json_file_to_list_content_elements(filepath: str) -> List[ProcessedNodeElement]:
    from inoft_vocal_framework.utils.general import load_json
    return botpress_diagrams_json_object_to_list_content_elements(list_all_node_elements=load_json(filepath))


def put_new_botpress_diagrams_data_from_list(nodes_list: list, projects_diagrams_data_dynamodb_client: ProjectsDiagramsDataDynamoDbClient):
    from inoft_vocal_engine.databases.dynamodb.projects_diagrams_data_dynamodb_client import NodeDatabaseItem

    nodes_list = botpress_diagrams_json_object_to_list_content_elements(list_all_node_elements=nodes_list)
    nodes_names_to_instances = dict()
    for node in nodes_list:
        nodes_names_to_instances[node.nodeName] = node

    for node in nodes_list:
        # todo: make ids dynamic
        db_node_item = NodeDatabaseItem(accountId="79120c34-b345-4718-b9b3-6ffece48ddea",
                                        accountProjectId="5aedb52e-3431-42dc-bf0b-ccd2844d2607",
                                        accountProjectInstanceId="test",
                                        nodeId=node.nodeId, nodeName=node.nodeName, actions=node.actions,
                                        transitions=node.transitions, temp_on_receive=node.temp_on_receive, nodeType=node.nodeType)
        projects_diagrams_data_dynamodb_client.put_new_node(node_item=db_node_item)

def put_new_botpress_diagrams_data_from_filepath(filepath: str, projects_diagrams_data_dynamodb_client: ProjectsDiagramsDataDynamoDbClient):
    nodes_list = botpress_diagrams_json_file_to_list_content_elements(filepath=filepath)
    put_new_botpress_diagrams_data_from_list(nodes_list=nodes_list, projects_diagrams_data_dynamodb_client=projects_diagrams_data_dynamodb_client)

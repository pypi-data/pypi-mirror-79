from typing import List, Dict

from pydantic import ValidationError

from inoft_vocal_engine.cloud_ressources.project_resources import ProjectResources
from inoft_vocal_engine.import_integrations.botpress.botpress_models import FlowFileBotpressModel, UiFileBotpressModel
from inoft_vocal_engine.safe_dict import SafeDict
from inoft_vocal_engine.import_integrations.botpress.engine_models import ContentElement, NodeDatabaseItem, \
    DatabaseTransitionConditionItem


class BotpressConverter:
    @staticmethod
    def convert_diagram_files(project_resources: ProjectResources, diagram_flow_data_dict: dict, diagram_ui_data_dict: dict):
        output_nodes_database_models: List[NodeDatabaseItem] = list()

        flow_populated_model_instance = None
        ui_populated_model_instance = None
        try:
            flow_populated_model_instance = FlowFileBotpressModel(**diagram_flow_data_dict)
            ui_populated_model_instance = UiFileBotpressModel(**diagram_ui_data_dict)
        except ValidationError as e:
            # todo: fix issues with validation errors. Instead of discaring the entire diagram when there is an
            #  error in one node, discard only the problematic node (BUT KEEP ALL THE VARIALE CHECKING !!!)
            print(e)

        if flow_populated_model_instance is not None and ui_populated_model_instance is not None:
            flow_ids_to_nodes: Dict[str, FlowFileBotpressModel.NodeModel] = dict()
            flow_names_to_nodes: Dict[str, FlowFileBotpressModel.NodeModel] = dict()
            for node in flow_populated_model_instance.nodes:
                flow_ids_to_nodes[node.id] = node
                flow_names_to_nodes[node.name] = node

            ui_ids_to_nodes: Dict[str, UiFileBotpressModel.NodePositionModel] = dict()
            for node in ui_populated_model_instance.nodes:
                ui_ids_to_nodes[node.id] = node

            for node_id, unique_node in flow_ids_to_nodes.items():
                unique_node_safedict = SafeDict(unique_node)
                try:
                    current_matching_node_position = ui_ids_to_nodes[unique_node.id]
                except Exception as e:
                    current_matching_node_position = None

                transition_conditions: List[DatabaseTransitionConditionItem] = list()
                if unique_node.next is not None:
                    for next_condition in unique_node.next:
                        # todo: check if a try except is faster than a in keys
                        current_next_condition_safedict = SafeDict(next_condition)
                        current_next_condition_target_condition = current_next_condition_safedict.get("condition").to_str(default=None)

                        current_next_condition_target_node_name = current_next_condition_safedict.get("node").to_str(default=None)
                        if current_next_condition_target_node_name in flow_names_to_nodes.keys():
                            current_next_condition_target_node_safedict = SafeDict(flow_names_to_nodes[current_next_condition_target_node_name])
                            current_next_item_outPortNodeId = current_next_condition_target_node_safedict.get("id").to_str(default=None)
                        else:
                            current_next_item_outPortNodeId = None

                        transition_conditions.append(DatabaseTransitionConditionItem(condition=current_next_condition_target_condition,
                                                                         targetNodeId=current_next_item_outPortNodeId))

                output_nodes_database_models.append(NodeDatabaseItem(
                    accountId=project_resources.account_username,  # todo: change incorrect use of account_username to account_id
                    accountProjectId=project_resources.account_project_id,
                    accountProjectInstanceId="12",
                    nodeId=unique_node.id,
                    nodeName=unique_node.name,
                    nodeType=unique_node.type,
                    actions=unique_node.onEnter,
                    transitions=transition_conditions,
                    temp_on_receive=unique_node.onReceive,
                    positionX=None if current_matching_node_position is None else current_matching_node_position.position.x,
                    positionY=None if current_matching_node_position is None else current_matching_node_position.position.y
                ))

        return output_nodes_database_models


    """"@staticmethod
    def botpress_node_to_engine_database_node(botpress_node: ):"""

    @staticmethod
    def botpress_contents_json_object_to_list_content_elements(list_all_text_elements: list) -> List[ContentElement]:
        from inoft_vocal_engine.inoft_vocal_markup.deserializer import Deserializer
        inoft_vocal_markup_deserializer = Deserializer(characters_names=["Léo", "Willie", "Menu"])

        content_elements: List[ContentElement] = list()
        for text_element in list_all_text_elements:
            current_content_element = ContentElement()
            current_content_element.character_names = list()

            text_element_safedict = SafeDict(text_element)
            text_content = text_element_safedict.get("formData").get("text$fr").to_str(default=None)
            if text_content is not None:
                current_content_element.crude_text = text_content
                current_content_element.dialogues_lines = inoft_vocal_markup_deserializer.deserialize(text=text_content)
                # todo: give the ability to select the language to deserialize

                for dialogue_line in current_content_element.dialogues_lines:
                    if dialogue_line.character_name is not None:
                        if dialogue_line.character_name not in current_content_element.character_names:
                            current_content_element.character_names.append(dialogue_line.character_name)
            else:
                current_content_element.crude_text = " "

            current_content_element.id = text_element_safedict.get("id").to_str(default=None)
            current_content_element.created_by = text_element_safedict.get("createdBy").to_str(default=None)
            current_content_element.created_on = text_element_safedict.get("createdOn").to_str(default=None)
            current_content_element.modified_on = text_element_safedict.get("modifiedOn").to_str(default=None)
            content_elements.append(current_content_element)

        return content_elements

    @staticmethod
    def botpress_json_file_to_list_content_elements(filepath: str) -> List[ContentElement]:
        from inoft_vocal_framework.utils.general import load_json
        return BotpressConverter.botpress_contents_json_object_to_list_content_elements(list_all_text_elements=load_json(filepath))

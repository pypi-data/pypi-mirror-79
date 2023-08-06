import ast
import os
from typing import Dict, List
import inflect as inflect

from inoft_vocal_engine.cloud_ressources.account_resources import AccountResources
from inoft_vocal_engine.cloud_ressources.engine_resources import EngineResources
from inoft_vocal_engine.cloud_ressources.project_resources import ProjectResources
from inoft_vocal_engine.code_generation.models import MessageItem, SetVariableAction, SayActionCodeGen
from inoft_vocal_engine.import_integrations.botpress.engine_models import ProcessedNodeElement, DatabaseTransitionConditionItem
from inoft_vocal_engine.models.actions import BaseAction, SayTextAction
from inoft_vocal_engine.safe_dict import SafeDict
from inoft_vocal_engine.utils.general import load_json
from inoft_vocal_engine.code_generation.templates.templates_access import TemplatesAccess

# todo: fix bug with node where no text is played (it will jump the node itself, and the next node x)  )


class GeneratorCore:
    def __init__(self, project_resources: ProjectResources):
        self.project_resources = project_resources
        self.nodes_elements = self.project_resources.project_diagrams_data_dynamodb_client.get_nodes_by_project_id(
            project_id="4addc838-a85d-4d43-a1bf-153e836f3a28"
        )

        self.has_conditions_classes = False
        self.has_request_handlers = False
        self.has_state_handlers = False
        self.messages = None

        self.threshold_of_intent_use_to_create_a_condition = 2

        self.counts_used_condition_intent_names = dict()
        self.node_ids_to_data_instances: Dict[str, ProcessedNodeElement] = dict()
        self.node_ids_to_components_instances = dict()

        self.templates = TemplatesAccess()
        self._plugins = None
        self.plugins_folder_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugins")

        self.say_actions: List[SayActionCodeGen] = list()
        self.set_variables_actions: List[SetVariableAction] = list()

    @property
    def plugins(self) -> list:
        if self._plugins is None:
            self.plugins_folder_dir = os.path.dirname(os.path.abspath(__file__))
        return list()

    def generate(self) -> List[str]:
        from inoft_vocal_engine.code_generation.components.launch_request_handler import LaunchRequestHandler
        from inoft_vocal_engine.code_generation.components.state_handler import StateHandler
        from inoft_vocal_engine.code_generation.components.intent_name_condition import IntentNameCondition
        from inoft_vocal_engine.code_generation.components.messages import Messages

        # self.messages = Messages(messages_items=load_json(self.builtin_text_filepath))
        # self.write_to_file(text=self.messages.render(parent_core=self), filepath="F:/Inoft/anvers_1944_project/inoft_vocal_engine/dist/messages.py")
        # os.path.join(os.path.dirname(os.path.abspath(__file__)), "messages.py"))

        # todo: re-implement logic of the startNode
        """
        flow_dict = load_json(filepath=self.main_flow_filepath)
        if "nodes" not in flow_dict.keys():
            raise Exception(f"The nodes key has not been found in the dict of the flow_file : {flow_dict}")
        else:
            name_start_node = flow_dict["startNode"]
            nodes_list = flow_dict["nodes"]
            # Initialization of the classes
        """

        for node in self.nodes_elements:
            self.node_ids_to_data_instances[node.nodeId] = node

            """if node_name == name_start_node:
                self.node_ids_to_components_instances[node_name] = LaunchRequestHandler(node_dict=node)
                self.has_request_handlers = True
            else:"""
            self.node_ids_to_components_instances[node.nodeId] = StateHandler(node_element=node)
            self.has_state_handlers = True

        # Processing of the classes and their interactions with each others
        for node_class in self.node_ids_to_components_instances.values():
            node_class.process(parent_core=self)

            if isinstance(node_class, StateHandler):
                for intent_key, count_value in node_class.counts_used_condition_intent_names.items():
                    if intent_key in self.counts_used_condition_intent_names.keys():
                        self.counts_used_condition_intent_names[intent_key] += count_value
                    else:
                        self.counts_used_condition_intent_names[intent_key] = count_value

        output_conditions_classes = list()
        for intent_key, count_value in self.counts_used_condition_intent_names.items():
            if count_value >= self.threshold_of_intent_use_to_create_a_condition:
                new_intent_name_condition_class = IntentNameCondition(intent_name=intent_key)
                new_intent_name_condition_class.render(parent_core=self)
                output_conditions_classes.append(new_intent_name_condition_class)
                self.has_conditions_classes = True

        output_handlers_list = list()
        for class_from_node in self.node_ids_to_components_instances.values():
            for handler_class in class_from_node.render(parent_core=self):
                output_handlers_list.append(handler_class)

        skill_app_rendered_code = self.templates.skill_app_template.render(conditions_classes_list=output_conditions_classes,
            handlers_list=output_handlers_list, has_condition_classes=self.has_conditions_classes,
            has_request_handlers=self.has_request_handlers, has_state_handlers=self.has_state_handlers)

        self.write_to_file(text=skill_app_rendered_code, filepath="F:/Inoft/anvers_1944_project/inoft_vocal_engine/dist/app_generated_v3.py")

        # todo: allow for the application to be saved across multiple files

        # todo: return the different files of each diagram in a dict with the key being the name of each diagram
        return [skill_app_rendered_code]

    def process_actions(self, actions_list: List[BaseAction]) -> list:
        self.say_actions.clear()
        logic_elements = list()

        for action in actions_list:
            if isinstance(action, SayTextAction):
                current_say_action = SayActionCodeGen(**action.dict())

                content_element = None
                if current_say_action.textContentItemId is not None:
                    content_element = self.project_resources.project_text_contents_dynamodb_client.get_by_element_id(
                        element_id=current_say_action.textContentItemId
                    )
                elif current_say_action.loadedTextToSay is not None:
                    # todo: add the use of element id in the say action, and remove this temporary shitty code
                    class TemporaryObject:
                        crudeText: str
                    content_element = TemporaryObject()
                    content_element.crudeText = current_say_action.loadedTextToSay

                if content_element is not None:
                    current_say_action.loadedTextToSay = content_element.crudeText
                    current_say_action.code = f"{current_say_action.loadedTextToSay}"
                    current_say_action.is_callable = False
                else:
                    current_say_action.text_to_say_if_message_item_missing = f"The message with id {current_say_action.textContentItemId} is missing"
                    current_say_action.is_callable = False

                logic_elements.append(self.templates.say_action_template.render(say_action=current_say_action, **current_say_action.extra_args))

                """
                if "/setVariable" in action:
                    processed_action_list = action.split('{', maxsplit=1)
                    if len(processed_action_list) > 1:
                        processed_action_dict = ast.literal_eval("{" + processed_action_list[1].replace("}", "") + "}")
                        if isinstance(processed_action_dict, dict):
                            if all(key in processed_action_dict.keys() and processed_action_dict[key] != "" for key in ["name", "value"]):
                                if "type" in processed_action_dict.keys() and processed_action_dict["type"] == "str":
                                    processed_action_dict["value"] = f'"{processed_action_dict["value"]}"'

                                logic_elements.append(self.templates.set_variable_logic_template.render(action_dict=processed_action_dict))
                """

        # from inoft_vocal_framework.plugins.OfficialAudioFilesInsteadOfText import Core as PluginCore
        # PluginCore().execute(generator_core=self)
        # todo: make it possible for the engine to use plugins, and create a new plugins system for the framework,
        #  that will not affect the code generation, but give the ability to add new functions to the framework.

        return logic_elements

    @staticmethod
    def write_to_file(text: str, filepath: str):
        with open(filepath, "w+", encoding="utf-8") as file:
            file.write(text)

if __name__ == "__main__":
    engine_resources = EngineResources()
    account_resources = AccountResources(engine_resources=engine_resources)
    project_resources = ProjectResources(engine_resources=engine_resources, account_resources=account_resources,
                                         project_url="anvers1944", project_owner_account_username="robinsonlabourdette",
                                         project_owner_account_id="b1fe5939-032b-462d-92e0-a942cd445096")
    GeneratorCore(project_resources=project_resources).generate()
    print("done")

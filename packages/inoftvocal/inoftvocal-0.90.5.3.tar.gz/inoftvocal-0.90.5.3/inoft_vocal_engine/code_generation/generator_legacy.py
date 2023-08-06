import ast
import os
from typing import Dict, List
import inflect as inflect

from inoft_vocal_engine.code_generation.models import MessageItem, SayAction, SetVariableAction
from inoft_vocal_engine.import_integrations.botpress.engine_models import ProcessedNodeElement, DatabaseTransitionConditionItem
from inoft_vocal_engine.safe_dict import SafeDict
from inoft_vocal_engine.utils.general import load_json
from inoft_vocal_engine.code_generation.templates.templates_access import TemplatesAccess

# todo: fix bug with node where no text is played (it will jump the node itself, and the next node x)  )


class GeneratorCore:
    def __init__(self, nodes_list: List[ProcessedNodeElement], main_flow_filepath: str = None, builtin_text_filepath: str = None):
        # self.main_flow_filepath = main_flow_filepath
        # self.builtin_text_filepath = builtin_text_filepath
        self.nodes_list = nodes_list

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

        self.say_actions: List[SayAction] = list()
        self.set_variables_actions: List[SetVariableAction] = list()

    @property
    def plugins(self) -> list:
        if self._plugins is None:
            self.plugins_folder_dir = os.path.dirname(os.path.abspath(__file__))
        return list()

    def generate(self):
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

        for node in self.nodes_list:
            self.node_ids_to_data_instances[node.node_name] = node

            """if node_name == name_start_node:
                self.node_ids_to_components_instances[node_name] = LaunchRequestHandler(node_dict=node)
                self.has_request_handlers = True
            else:"""
            self.node_ids_to_components_instances[node.node_name] = StateHandler(node_name=node.node_name)
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

        return skill_app_rendered_code

        # self.write_to_file(text=skill_app_rendered_code, filepath="F:/Inoft/anvers_1944_project/inoft_vocal_engine/dist/app_generated.py")

    def process_on_enter(self, actions_list: list) -> list:
        self.say_actions.clear()
        logic_elements = list()

        for action in actions_list:
            if isinstance(action, str):
                if len(action) >= 3:
                    if action[0:3] == "say":
                        if "#!builtin_text" in action:
                            current_say_action = SayAction()
                            current_say_action.message_id_to_say = action.replace("say", "").replace("#!", "").replace(" ", "")

                            if current_say_action.message_id_to_say in self.messages.output_messages_dict.keys():
                                current_say_action.message_item_to_say = self.messages.output_messages_dict[current_say_action.message_id_to_say]
                            else:
                                current_say_action.text_to_say_if_message_item_missing = f"The message with id {current_say_action.message_id_to_say} is missing"

                            self.say_actions.append(current_say_action)

                if "/setVariable" in action:
                    processed_action_list = action.split('{', maxsplit=1)
                    if len(processed_action_list) > 1:
                        processed_action_dict = ast.literal_eval("{" + processed_action_list[1].replace("}", "") + "}")
                        if isinstance(processed_action_dict, dict):
                            if all(key in processed_action_dict.keys() and processed_action_dict[key] != "" for key in ["name", "value"]):
                                if "type" in processed_action_dict.keys() and processed_action_dict["type"] == "str":
                                    processed_action_dict["value"] = f'"{processed_action_dict["value"]}"'

                                logic_elements.append(self.templates.set_variable_logic_template.render(action_dict=processed_action_dict))

        # from inoft_vocal_framework.plugins.OfficialAudioFilesInsteadOfText import Core as PluginCore
        # PluginCore().execute(generator_core=self)
        # todo: make it possible for the engine to use plugins, and create a new plugins system for the framework,
        #  that will not affect the code generation, but give the ability to add new functions to the framework.

        for say_action in self.say_actions:
            if say_action.code is None:
                if say_action.message_item_to_say is not None:
                    say_action.code = f"{say_action.message_item_to_say.variable_name}.pick()"
                    say_action.is_callable = True
                else:
                    say_action.code = say_action.text_to_say_if_message_item_missing
                    say_action.is_callable = False

            logic_elements.append(self.templates.say_action_template.render(say_action=say_action, **say_action.extra_args))

        return logic_elements

    @staticmethod
    def write_to_file(text: str, filepath: str):
        with open(filepath, "w+", encoding="utf-8") as file:
            file.write(text)

if __name__ == "__main__":
    GeneratorCore(nodes_list=list(),
        main_flow_filepath="F:/Inoft/anvers_1944_project/inoft_vocal_engine/code_generation/main.flow.json",
        builtin_text_filepath="F:/Inoft/anvers_1944_project/inoft_vocal_engine/code_generation/builtin_text.json"
                  ).generate()
    print("done")

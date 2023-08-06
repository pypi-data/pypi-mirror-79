from typing import Optional, Any
from pydantic import BaseModel


class BaseAction(BaseModel):
    _TYPE_NAME = "base"

    isNew: bool = False
    nodeId: str
    actionType: str
    _FIELDS_TO_EXCLUDE: set = {"isNew", "nodeId"}

    def to_database(self) -> dict:
        return self.dict(exclude=self._FIELDS_TO_EXCLUDE)


class SayTextAction(BaseAction):
    _TYPE_NAME = "sayText"

    textContentItemId: Optional[str]
    loadedTextToSay: Optional[str]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super()._FIELDS_TO_EXCLUDE.add("loadedTextToSay")

    # todo: deprecated
    @classmethod
    def make_new(cls, text_content_id: Optional[str], **kwargs):
        return cls(textContentItemId=text_content_id, **kwargs)

class UserDataMemorizeVariableAction(BaseAction):
    _TYPE_NAME = "userDataMemorizeVariable"

    variableName: Optional[str]
    variableType: Optional[str]


actions_keys_switch = {
    BaseAction._TYPE_NAME: BaseAction,
    SayTextAction._TYPE_NAME: SayTextAction,
    UserDataMemorizeVariableAction._TYPE_NAME: UserDataMemorizeVariableAction
}

def get_appropriate_action_from_dict(action_data_dict: dict) -> Optional[BaseAction]:
    if "actionType" in action_data_dict.keys():
        action_class_type = actions_keys_switch.get(action_data_dict["actionType"], None)
        if action_class_type is not None:
            return action_class_type(**action_data_dict)
    return None




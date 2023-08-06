from dataclasses import field
from typing import Optional
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from inoft_vocal_engine.models.actions import SayTextAction


@dataclass
class MessageItem:
    id: str
    speech_items: Optional[list] = None
    is_callable: Optional[bool] = False
    variable_name: str = None

    def __post_init_post_parse__(self):
        if isinstance(self.id, str):
            self.variable_name = "".join([char.capitalize() for char in self.id.replace("-", "_")])
        else:
            self.variable_name = None

class SayActionCodeGen(SayTextAction):
    is_callable: bool = False
    text_to_say_if_message_item_missing: Optional[str] = "A message element is missing."
    code: str = None
    extra_args: dict = dict()

class SetVariableAction:
    def __init__(self):
        pass
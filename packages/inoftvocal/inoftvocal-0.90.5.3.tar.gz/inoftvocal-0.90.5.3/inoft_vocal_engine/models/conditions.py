from pydantic import BaseModel


class BaseCondition(BaseModel):
    conditionType: str

class ConditionIsIntentName(BaseCondition):
    _TYPE = "IS-INTENT-NAME"
    intentName: str

    def __init__(self, **kwargs):
        super().__init__(conditionType=self._TYPE, **kwargs)

class ConditionAlways(BaseCondition):
    _TYPE = "ALWAYS"

    def __init__(self, **kwargs):
        super().__init__(conditionType=self._TYPE, **kwargs)

class ConditionMemoryVariableExpression(BaseCondition):
    _TYPE = "MEMORY-VARIABLE-EXPRESSION"
    memoryType: str
    variableName: str
    conditionExpression: str

    def __init__(self, **kwargs):
        super().__init__(conditionType=self._TYPE, **kwargs)

def get_appropriate_condition(condition_data: dict):
    # todo: improve this code
    if isinstance(condition_data, dict) and "conditionType" in condition_data.keys():
        condition_type = condition_data["conditionType"]
        condition_data.pop("conditionType")

        if condition_type == ConditionIsIntentName._TYPE:
            return ConditionIsIntentName(**condition_data)
        elif condition_type == ConditionAlways._TYPE:
            return ConditionAlways(**condition_data)
        elif condition_type == ConditionMemoryVariableExpression._TYPE:
            return ConditionMemoryVariableExpression(**condition_data)
    return None

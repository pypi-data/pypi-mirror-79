from dataclasses import field
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from pydantic.dataclasses import dataclass
from inoft_vocal_engine.inoft_vocal_markup.deserializer import DialogueLine
from inoft_vocal_engine.models.actions import BaseAction
from inoft_vocal_engine.models.conditions import BaseCondition


class ContentElement(BaseModel):
    id: str = None
    created_by: str = None
    created_on: str = None
    modified_on: str = None
    crude_text: str = None
    character_names: list = None
    dialogues_lines: Optional[List[DialogueLine]] = None

class DatabaseTransitionConditionItem(BaseModel):
    transitionId: str = None
    condition: Optional[dict] = None
    sourceNodeId: Optional[str] = None
    targetNodeId: Optional[str] = None

    """@validator("condition")
    def get_appropriate_condition(cls, value):
        from inoft_vocal_engine.models.conditions import get_appropriate_condition
        return get_appropriate_condition(condition_data=value)"""

    def to_database(self) -> dict:
        return self.dict(exclude={"transitionId", "sourceNodeId"})

class ProcessedTransitionCondition(BaseModel):
    transitionId: str
    condition: Optional[BaseCondition] = None
    sourceNodeId: Optional[str] = None
    targetNodeId: Optional[str] = None

    @classmethod
    def from_database_item(cls, database_transition_condition_item: DatabaseTransitionConditionItem):
        from inoft_vocal_engine.models.conditions import get_appropriate_condition
        return cls(
            transitionId=database_transition_condition_item.transitionId,
            condition=get_appropriate_condition(database_transition_condition_item.condition),
            sourceNodeId=database_transition_condition_item.sourceNodeId,
            targetNodeId=database_transition_condition_item.targetNodeId
        )

class ProcessedNodeElement(BaseModel):
    nodeId: str = None
    nodeName: str = "Unnamed"
    actions: Optional[List[BaseAction]] = list()
    transitions: Optional[List[ProcessedTransitionCondition]] = list()
    temp_on_receive: Optional[list] = list()
    nodeType: str = None
    positionX: int = 0
    positionY: int = 0
    # todo: make stricter variables validation

class NodeElementDataReceivedFromUser(BaseModel):
    nodeId: str
    nodeName: Optional[str] = None
    actions: Optional[List[dict]]
    transitions: Optional[Dict[str, DatabaseTransitionConditionItem]]
    temp_on_receive: Optional[list] = None
    nodeType: Optional[str] = None
    positionX: Optional[int] = None
    positionY: Optional[int] = None

class NodeDatabaseItem(BaseModel):
    accountId: str
    accountProjectId: str
    accountProjectInstanceId: str
    nodeId: str
    nodeName: str
    positionX: int = 0
    positionY: int = 0
    nodeType: str = None
    actions: List[dict] = dict()  # todo: create a database action item
    transitions: Dict[str, dict] = dict()
    temp_on_receive: Optional[list] = list()

    def to_processed_node_element(self) -> ProcessedNodeElement:
        from inoft_vocal_engine.models.actions import get_appropriate_action_from_dict
        # The way the actions are stored in the database for the way the data is structured in the client
        # browser. In the browser, all the data (nodeId, actionId) is in the same object for simpler sending
        # to the database, where as in the database, we do not duplicate data if there is no need to.
        processed_actions: List[BaseAction] = list()
        for action in self.actions:
            action["nodeId"] = self.nodeId
            action["isNew"] = False

            action_instance = get_appropriate_action_from_dict(action_data_dict=action)
            if action_instance is not None:
                processed_actions.append(action_instance)

        processed_transitions: List[ProcessedTransitionCondition] = list()
        for transition_key_id, transition_values in self.transitions.items():
            processed_transitions.append(ProcessedTransitionCondition.from_database_item(
                DatabaseTransitionConditionItem(transitionId=transition_key_id, sourceNodeId=self.nodeId, **transition_values)
            ))

        return ProcessedNodeElement(
            nodeId=self.nodeId,
            nodeName=self.nodeName,
            actions=processed_actions,
            transitions=processed_transitions,
            temp_on_receive=self.temp_on_receive,
            nodeType=self.nodeType,
            positionX=self.positionX,
            positionY=self.positionY
        )


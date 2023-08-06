from typing import List, Optional

from pydantic import BaseModel
from pydantic.dataclasses import dataclass


class FlowFileBotpressModel(BaseModel):
    class NodeModel(BaseModel):
        id: str
        name: str = None
        type: str = None
        next: Optional[List[dict]] = None
        onEnter: Optional[List[str]] = None
        onReceive: Optional[List[str]] = None
    version: str
    catchAll: dict
    startNode: str
    description: Optional[str] = None
    nodes: Optional[List[NodeModel]] = list()

class UiFileBotpressModel(BaseModel):
    class NodePositionModel(BaseModel):
        class PositionModel(BaseModel):
            x: int
            y: int
        id: str
        position: Optional[PositionModel] = PositionModel(x=0, y=0)
    nodes: Optional[List[NodePositionModel]] = None

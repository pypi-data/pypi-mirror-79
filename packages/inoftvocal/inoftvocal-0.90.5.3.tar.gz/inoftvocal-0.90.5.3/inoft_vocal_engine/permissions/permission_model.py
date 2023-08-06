from dataclasses import dataclass
from typing import Optional


@dataclass
class PermissionModel:
    expression: str
    display_name: str
    description: Optional[str] = None
    additional_kwargs: Optional[dict] = None

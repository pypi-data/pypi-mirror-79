from typing import Optional
from pydantic import BaseModel


class BackendReceivedProjectData(BaseModel):
    projectName: str
    projectPrimaryUrl: str
    projectDescription: Optional[str] = None

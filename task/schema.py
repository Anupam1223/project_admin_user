from pydantic import BaseModel
from typing import Optional
from enum import Enum

# -----model to validate task, aslo used for creating task,
# and for the response----------------------------------------
class Create_task(BaseModel):
    Task_id: int
    Task_name: str
    project_name: int
    description: str
    project_created_by: int
    project_assigned_to: int
    progress: str


# ------------------------------------------------------------

# ------------- Stages of progress----------------------------
class Progress(str, Enum):
    block = "block"
    assign = "assign"
    complete = "complete"


# ------------------------------------------------------------

# ----To take in progress value that we want to update-------
class Update_progress(BaseModel):
    progress: Progress


# ------------------------------------------------------------

# ------------For manipulating token data---------------------
class TokenData(BaseModel):
    username: Optional[str] = None


# ------------------------------------------------------------

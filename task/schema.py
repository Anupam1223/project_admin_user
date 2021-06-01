from pydantic import BaseModel
from typing import Optional

# -----model to validate task, aslo used for creating task,
# and for the response----------------------------------------
class Create_task(BaseModel):
    Task_name: str
    project_name: str
    description: str
    project_created_by: str
    project_assigned_to: str
    progress: str


# ------------------------------------------------------------

# ----To take in progress value that we want to update-------
class Update_progress(BaseModel):
    progress: str


# ------------------------------------------------------------

# ------------For manipulating token data---------------------
class TokenData(BaseModel):
    username: Optional[str] = None


# ------------------------------------------------------------

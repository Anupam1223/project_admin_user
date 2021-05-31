from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class Create_task(BaseModel):
    task_name: str
    project_name: str
    description: str
    project_created_by: str
    project_assigned_to: str


class view_assigned_project(BaseModel):
    Task_name: str
    project_name: str
    description: str
    project_created_by: str
    project_assigned_to: str


class TokenData(BaseModel):
    username: Optional[str] = None

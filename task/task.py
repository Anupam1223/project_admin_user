from initialize import models
from fastapi import Depends, HTTPException, status, APIRouter
from .schema import Create_task, TokenData, Update_progress
from . import crud
from user.user import oauth2_scheme, get_user
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Dict
from fastapi.encoders import jsonable_encoder
from sqlalchemy import engine
from initialize.database import engine


models.Base.metadata.create_all(bind=engine)
router = APIRouter()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

# ---------------common method to undo token------------------------------------
def undo_token(token):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("user")
        if username is None:
            return {"Error!!!": "Provided name is not a user"}
        token_data = TokenData(username=username).username
        return token_data
    except JWTError:
        raise credentials_exception


# ------------------------------------------------------------------------------

# -------------------View if admin else dont give permission-------------------
def get_admin_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_user)
):
    token_info = undo_token(token)
    view_user_project = crud.check_admin(db, username=token_info)
    if view_user_project is None:
        return {"Error!!!": "Provided user is not admin"}
    return view_user_project


@router.get("/view_user_project_as_admin", tags=["Task"])
async def view_user_project_as_admin(
    user_project: Dict = Depends(get_admin_user),
):
    return user_project


# -----------------------------------------------------------------------------

# ------ view the user profile-------------------------------------------------
def get_user_project(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_user)
):
    token_info = undo_token(token)
    view_user_project = crud.return_user(db, username=token_info)
    return view_user_project


@router.get("/view_user_project_as_user", tags=["Task"])
async def view_user_project_as_user(
    user_project: Dict = Depends(get_user_project),
):
    return user_project


# -----------------------------------------------------------------------------

# ---------Add task by admin---------------------------------------------------
@router.post("/create_task", tags=["Task"])
async def create_task(
    task: Create_task,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_user),
):
    token_info = undo_token(token)
    view_user_project = crud.check_admin(db, username=token_info)
    if view_user_project is None:
        return {"Error": "User is not Admin"}
    crud.create_task_for_user(db, task)
    return {"success!!": "Task inserted seccessfully"}


# -----------------------------------------------------------------------------

# --------update the status of the task----------------------------------------
@router.put("/update_task_progression/{Name_Of_Programmer}", tags=["Task"])
async def update_task(
    Name_Of_Programmer: int,
    update_progress: Update_progress,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_user),
):

    token_info = undo_token(token)
    view_user_project = crud.check_admin(db, username=token_info)
    if view_user_project is None:
        return {"Error": "Only admin is allowed to update"}
    updated_value = crud.update_progress(db, update_progress, Name_Of_Programmer)
    if updated_value:
        return {"Success!!": "Record updated successfully"}
    return {"Error!!": "Update terminated"}


# ------------------------------------------------------------------------------

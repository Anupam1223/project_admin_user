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
from typing import Optional


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
    return jsonable_encoder(view_user_project)


@router.get("/view_user_project_as_admin", tags=["View Task"])
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
    return jsonable_encoder(view_user_project)


@router.get("/view_user_project_as_user", tags=["View Task"])
async def view_user_project_as_user(
    user_project: Dict = Depends(get_user_project),
):
    return user_project


# -----------------------------------------------------------------------------

# ---------Add task by admin---------------------------------------------------
@router.post("/create_task", tags=["Create Task"])
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

# --------update the status of the task as admin----------------------------------------
@router.put("/update_task_progression/", tags=["Update Progress"])
async def update_task(
    update_progress: Update_progress,
    token: str = Depends(oauth2_scheme),
    userid_of_programmer: Optional[int] = None,
    db: Session = Depends(get_user),
):

    value_to_update = update_progress.progress
    token_info = undo_token(token)

    is_admin = crud.check_admin(db, username=token_info)

    if is_admin is None:
        user_value = (
            db.query(models.Login).filter(models.Login.username == token_info).first()
        )
        user_id = user_value.user_id
        updated_value = crud.update_progress(db, value_to_update, user_id)
        if updated_value:
            return {"Success!!": "Record updated successfully"}
        return {"Error!!": "Update terminated"}

    updated_value = crud.update_progress(db, value_to_update, userid_of_programmer)
    if updated_value:
        return {"Success!!": "Record updated successfully"}
    return {"Error!!": "Update terminated"}


# ------------------------------------------------------------------------------

# --------view task and assigned programmer-------------------------------------
@router.get("/view_task_programmer", tags=["View Task"])
async def view_task_programmer(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_user),
):
    token_info = undo_token(token)
    is_admin = crud.check_admin(db, username=token_info)
    if is_admin is None:
        programmer = crud.return_user(db, token_info)
        project_id = programmer.project_name
        project_assigned_to = programmer.project_assigned_to
        project_name = (
            db.query(models.Project)
            .filter(models.Project.project_id == project_id)
            .first()
        )
        user_name = (
            db.query(models.Login)
            .filter(models.Login.user_id == project_assigned_to)
            .first()
        )
        return {
            "username": user_name.first_name,
            "project name": project_name.project_name,
        }

    project_names = []
    user_names = []
    project_user_dict = {}

    for programmer in is_admin:
        id = programmer.project_name
        work_is_done_by = programmer.project_assigned_to
        project_name = (
            db.query(models.Project).filter(models.Project.project_id == id).first()
        )
        user_name = (
            db.query(models.Login)
            .filter(models.Login.user_id == work_is_done_by)
            .first()
        )
        project_names.append(project_name.project_name)
        user_names.append(user_name.first_name)

    for key in user_names:
        for value in project_names:
            project_user_dict[key] = value
            project_names.remove(value)
            break

    return project_user_dict

from initialize import models
from fastapi import Depends, HTTPException, status, APIRouter
from .schema import Create_task, TokenData, Update_progress, Progress
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

# ---------------common method to undo and return token------------------------------------
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
    """
    depends upon oauth2_scheme for authorization token sent from post method
    (verify_stored_user) of user module, also depends upon function(get_user)
    for setting database connection.checks if the user trying to access the
    endpoint is admin or not,if not admin then returns error else returns
    all the record of all the programmer
    """
    token_info = undo_token(token)
    view_user_project = crud.check_admin(db, username=token_info)
    if view_user_project is None:
        return {"Error!!!": "Provided user is not admin"}
    return jsonable_encoder(view_user_project)


@router.get("/view_user_project_as_admin", tags=["View Task"])
async def view_user_project_as_admin(
    user_project: Dict = Depends(get_admin_user),
):
    """
    depends upon get_admin_user, which returns Dictionary value of all the
    user data present in task table

    *authentication is required
    """
    return user_project


# -----------------------------------------------------------------------------

# ------ view the user profile-------------------------------------------------
def get_user_project(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_user)
):
    """
    depends upon oauth2_scheme for authorization token sent from post method
    (verify_stored_user) of user module, also depends upon function(get_user)
    for setting database connection

    """
    token_info = undo_token(token)
    view_user_project = crud.return_user(db, username=token_info)
    return jsonable_encoder(view_user_project)


@router.get("/view_user_project_as_user", tags=["View Task"])
async def view_user_project_as_user(
    user_project: Dict = Depends(get_user_project),
):
    """
    depends upon get_user_project, which returns Dictionary value of user data

    *authentication is required
    """
    return user_project


# -----------------------------------------------------------------------------

# ---------Add task by admin---------------------------------------------------
@router.post("/create_task", tags=["Create Task"])
async def create_task(
    task: Create_task,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_user),
):
    """
    depends upon oauth2_scheme for authorization token sent from post method
    (verify_stored_user) of user module, also depends upon function(get_user)
    for setting database connection.
    task, which is declared as Create_task model, Create_task is a pydantic model
    inside schema module

    *authentication is required
    """
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
    """
    depends upon oauth2_scheme for authorization token sent from post method
    (verify_stored_user) of user module, also depends upon function(get_user)
    for setting database connection.This function works for both admin and programmer

         user
            *)simply your token will be decoded, check your detail, retrieve user_id and
            then use ORM query to update the task of this user with the help user_id in
            task table, you can update only your progress and you dont have to privide
            query parameter
         admin
            *) you pass user_id of the programmer in query paramater and then use this to
            update the progress of the provided user

    *authentication is required
    """
    if update_progress.progress not in Progress.__members__:
        return {"Error!!": "Choose among 'assign', 'rollback', 'block', 'complete' "}

    value_to_update = update_progress.progress
    token_info = undo_token(token)

    is_admin = crud.check_admin(db, username=token_info)

    if is_admin is None:
        user_value = (
            db.query(models.Login).filter(models.Login.username == token_info).first()
        )
        user_id = user_value.user_id
        user_status = user_value.status
        if user_status == True:
            updated_value = crud.update_progress(db, value_to_update, user_id)
            if updated_value:
                return {"Success!!": "Record updated successfully"}
            return {"Error!!": "Update terminated"}
        return {"Error!!": "User is not active"}

    updated_value = crud.update_progress(db, value_to_update, userid_of_programmer)
    if updated_value:
        return {"Success!!": "Record updated successfully"}
    return {
        "Error!!": "Update terminated, if your are admin the pass query parameter (Userid_Of_Programmer) of the user you want to update"
    }


# ------------------------------------------------------------------------------

# --------view task and assigned programmer-------------------------------------
@router.get("/view_task_programmer", tags=["View Task"])
async def view_task_programmer(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_user),
):
    """
    takes in token and session to connect with database,
    if the accessing user is programmer then he/she can see
    the task they are assigned with, if admin is accessing then
    he/she can see all the programmer according to their repective
    project

    *authentication is required
    """
    # token_info() decode the jwt token and return the name of the
    # user accessing this end-point
    token_info = undo_token(token)

    # checks if the user is admin or not
    is_admin = crud.check_admin(db, username=token_info)

    if is_admin is None:

        # return_user() of CRUD returns the object of the accessing
        # user from our database, and is stored in programmer variacle
        programmer = crud.return_user(db, token_info)

        # retrieve the project id from the object programmer
        project_id = programmer.project_name

        # retrieve the user id from the object programmer
        project_assigned_to = programmer.project_assigned_to

        # query to get the project name from Project ORM table
        project_name = (
            db.query(models.Project)
            .filter(models.Project.project_id == project_id)
            .first()
        )

        # query to get the username name from Login ORM table
        user_name = (
            db.query(models.Login)
            .filter(models.Login.user_id == project_assigned_to)
            .first()
        )

        # returns the username of the user and the task given to him
        # in the form of dictionary
        return {
            "username": user_name.first_name,
            "project name": project_name.project_name,
        }

    # this part of code runs if the accesing user is admin

    # project_names[], this list is created to store the project names assigned to the programmer
    project_names = []

    # user_names[], this list is created to store the names of the programmer
    user_names = []

    # project_user_dict[], this dictionary is created for returning the obtained values in dictionary
    project_user_dict = {"Programmer": "Task"}

    # we iterate through the is_admin object, which contains all the data or rows from task table
    # we do this to fetch project names and user names
    for programmer in is_admin:
        # id and work_is_done_by strores the project_id and project_assigned_to from the first index
        # of is_admin, this value is upgraded to its successor on each round
        id = programmer.project_name
        work_is_done_by = programmer.project_assigned_to

        # runs the query from project table and filters only those projects which are assigned to the
        # programmer
        project_name = (
            db.query(models.Project).filter(models.Project.project_id == id).first()
        )

        # runs the query from Login table and filters only those Programmers which are assigned to the
        # task
        user_name = (
            db.query(models.Login)
            .filter(models.Login.user_id == work_is_done_by)
            .first()
        )

        # above obtained project and programmer names are stored in this lists
        project_names.append(project_name.project_name)
        user_names.append(user_name.first_name)

    # merging two list to form a dictionary so that we can return this dictionary
    for key in user_names:
        for value in project_names:
            project_user_dict[key] = value
            project_names.remove(value)
            break

    return project_user_dict


# ----------------------------------------------------------------------------------

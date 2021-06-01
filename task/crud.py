from sqlalchemy.orm import Session
from initialize import models
from . import schema
from fastapi.encoders import jsonable_encoder

# ------check and return all the data regarding project and user --------------
def check_admin(db: Session, username):
    """
    Takes in session and username in string as parameter and
    Checks whether the username that we get from token is
    admin or not, if he/she is admin then all the task
    related record is returned, else None is returned
    """
    user_value = (
        db.query(models.Login).filter(models.Login.username == username).first()
    )
    admin = user_value.super_user
    status = user_value.status
    if admin == True:
        if status == True:
            project_assigned = db.query(models.Task).all()
            user_dict = jsonable_encoder(project_assigned)
            return user_dict
        return {"Error!!": "User is not active"}
    return None


# -----------------------------------------------------------------------------

# ---------------return particular user and related task-----------------------
def return_user(db: Session, username):
    """
    Takes in session and username as parameter in string and
    Checks whether the username that we get from token is
    active or not, if he/she is active then task record
    related to the user is returned, else error message is returned
    """
    user_value = (
        db.query(models.Login).filter(models.Login.username == username).first()
    )
    user = user_value.first_name
    available = user_value.status
    if available:
        user_and_project = (
            db.query(models.Task)
            .filter(models.Task.project_assigned_to == user)
            .first()
        )
        return jsonable_encoder(user_and_project)
    return {"Error!!!!": "User is not active"}


# ------------------------------------------------------------------------------

# -------------------admin can create task--------------------------------------
def create_task_for_user(db: Session, create: schema.Create_task):
    """
    Takes in session and Create_task schema from schema model and
    insert the values brought by this model in our databse table "task"
    """
    db_task = models.Task(
        Task_name=create.Task_name,
        project_name=create.project_name,
        description=create.description,
        project_created_by=create.project_created_by,
        project_assigned_to=create.project_assigned_to,
        progress=create.progress,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


# -------------------------------------------------------------------------------

# ---------------------update the progress----------------------------------------
def update_progress(
    db: Session, update_progress: schema.Update_progress, Name_Of_Programmer: str
):
    """
    Takes in session and Update_progress schema from schema model and
    Name_Of_Programmer as string and then update the progress of this programmer
    """
    updated_value = (
        db.query(models.Task)
        .filter(models.Task.project_assigned_to == Name_Of_Programmer)
        .update({"progress": update_progress})
    )
    db.commit()
    return updated_value


# ---------------------------------------------------------------------------------

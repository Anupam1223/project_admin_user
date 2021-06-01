from sqlalchemy.orm import Session
from initialize import models
from . import schema
from fastapi.encoders import jsonable_encoder

# ------check and return all the data regarding project and user --------------
def check_admin(db: Session, username):
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
    updated_value = (
        db.query(models.Task)
        .filter(models.Task.project_assigned_to == Name_Of_Programmer)
        .update({"progress": update_progress})
    )
    db.commit()
    print(type(updated_value))
    return updated_value


# ---------------------------------------------------------------------------------

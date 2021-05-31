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
    if admin == True:
        project_assigned = db.query(models.Task).all()
        user_dict = jsonable_encoder(project_assigned)
        return user_dict
    return False


# -----------------------------------------------------------------------------

# ---------------return particular user and related task-----------------------
def return_user(db: Session, username):
    user_value = (
        db.query(models.Login).filter(models.Login.username == username).first()
    )
    user = user_value.first_name
    user_and_project = (
        db.query(models.Task).filter(models.Task.project_assigned_to == user).first()
    )
    return jsonable_encoder(user_and_project)


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

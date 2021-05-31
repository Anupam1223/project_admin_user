from sqlalchemy.orm import Session
from initialize import models
from . import schema
from fastapi.encoders import jsonable_encoder


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

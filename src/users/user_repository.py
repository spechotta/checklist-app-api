from sqlalchemy.orm import Session
from src.users import user_models
from src.users.user_schemas import User


def get_all_users(db: Session):
    return db.query(user_models.User).all()

def create_user(user: user_models.User, db: Session):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(user_id: int, db: Session):
    return db.query(user_models.User).filter(user_models.User.id == user_id).first()

def save_user(db_user: User, db: Session):
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db_user: User, db: Session):
    db.delete(db_user)
    db.commit()
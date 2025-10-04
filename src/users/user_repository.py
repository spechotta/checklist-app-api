from sqlalchemy.orm import Session
from src.users import user_models
from src.users.user_schemas import User


def get_all_users(db: Session):
    return db.query(user_models.User).all()

def create_user(user: User, db: Session):
    db_user = user_models.User(
        firstName = user.firstName,
        lastName = user.lastName,
        email = user.email,
        hashedPassword = user.hashedPassword
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(user_id: int, db: Session):
    return db.query(user_models.User).filter(user_models.User.id == user_id).first()

def save_user(db_user: User, db: Session):
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db_user: User, db: Session):
    db.delete(db_user)
    db.commit()
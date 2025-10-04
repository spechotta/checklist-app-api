from sqlalchemy.orm import Session
from src.users import user_repository
from src.users.user_exceptions import UserNotFoundException
from src.users.user_schemas import User


def get_users(db: Session):
    return user_repository.get_all_users(db)

def create_user(user_create: User, db: Session):
    db_user = user_create.dto_to_orm()
    return user_repository.create_user(db_user, db)

def get_user(user_id: int, db: Session):
    db_user = user_repository.get_user_by_id(user_id, db)
    if not db_user:
        raise UserNotFoundException(user_id)
    return db_user

def update_user(user_id: int, user_update: User, db: Session):
    db_user = user_repository.get_user_by_id(user_id, db)
    if not db_user:
        raise UserNotFoundException(user_id)

    user_update.dto_to_orm(db_user)
    return user_repository.save_user(db_user, db)

def delete_user(user_id: int, db: Session):
    db_user = user_repository.get_user_by_id(user_id, db)
    if not db_user:
        raise UserNotFoundException(user_id)
    user_repository.delete_user(db_user, db)
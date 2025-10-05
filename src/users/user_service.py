from sqlalchemy.orm import Session
from src.users import user_repository
from src.users.user_exceptions import UserNotFoundException
from src.users.user_schemas import User, UserResponse


def get_users(db: Session):
    db_users = user_repository.get_all_users(db)
    user_dtos = []

    for user in db_users:
        user_dto = UserResponse.orm_to_dto(user)
        user_dtos.append(user_dto)

    return user_dtos

def create_user(new_user: User, db: Session):
    user_entity = new_user.dto_to_orm()
    created_user = user_repository.create_user(user_entity, db)
    return UserResponse.orm_to_dto(created_user)

def get_user(user_id: int, db: Session):
    db_user = user_repository.get_user_by_id(user_id, db)
    if not db_user:
        raise UserNotFoundException(user_id)
    return UserResponse.orm_to_dto(db_user)

def update_user(user_id: int, existing_user: User, db: Session):
    db_user = user_repository.get_user_by_id(user_id, db)
    if not db_user:
        raise UserNotFoundException(user_id)

    existing_user.dto_to_orm(db_user)
    updated_user = user_repository.save_user(db_user, db)
    return UserResponse.orm_to_dto(updated_user)

def delete_user(user_id: int, db: Session):
    db_user = user_repository.get_user_by_id(user_id, db)
    if not db_user:
        raise UserNotFoundException(user_id)
    user_repository.delete_user(db_user, db)
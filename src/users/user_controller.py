from typing import List
from fastapi import APIRouter, status, Response
from src.users import user_service
from src.users.user_schemas import User, UserResponse
from src.dependencies import DbSession


router = APIRouter(prefix = "/users", tags = ["Users"])

@router.get("", status_code = status.HTTP_200_OK, response_model = List[UserResponse])
def get_users(db: DbSession):
    return user_service.get_users(db)

@router.post("", status_code = status.HTTP_201_CREATED, response_model = UserResponse)
def create_user(user: User, db: DbSession):
    return user_service.create_user(user, db)

@router.get("/{user_id}", status_code = status.HTTP_200_OK, response_model = UserResponse)
def get_user(user_id: int, db: DbSession):
    return user_service.get_user(user_id, db)

@router.put("/{user_id}", status_code = status.HTTP_200_OK, response_model = UserResponse)
def update_user(user_id: int, user: User, db: DbSession):
    return user_service.update_user(user_id, user, db)

@router.delete("/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: DbSession):
    user_service.delete_user(user_id, db)
    return Response(status_code = status.HTTP_204_NO_CONTENT)
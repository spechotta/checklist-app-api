from typing import List, Optional
from pydantic import BaseModel, EmailStr
from src.users import models as user_models


class User(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    hashedPassword: str

    def dto_to_orm(self, existing_user: Optional[user_models.User] = None) -> user_models.User:
        if existing_user is None:
            return self._create_user()
        return self._update_user(existing_user)

    def _create_user(self) -> user_models.User:
        return user_models.User(
            firstName = self.firstName,
            lastName = self.lastName,
            email = self.email,
            hashedPassword = self.hashedPassword
        )

    def _update_user(self, existing_user: user_models.User) -> user_models.User:
        existing_user.firstName = self.firstName
        existing_user.lastName = self.lastName
        existing_user.email = self.email
        existing_user.hashedPassword = self.hashedPassword
        return existing_user

class UserResponse(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: EmailStr
    checklist_ids: List[int] = []

    class Config:
        from_attributes = True
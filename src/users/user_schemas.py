from typing import List, Optional
from pydantic import BaseModel, EmailStr
from src.users import user_models


class User(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    hashedPassword: str
    checklist_ids: List[int] = []

    def dto_to_orm(self, existing_user: Optional[user_models.User] = None) -> user_models.User:
        if existing_user is None:
            return self._create_user()
        return self._update_user(existing_user)

    def _create_user(self) -> user_models.User:
        user = user_models.User(
            firstName = self.firstName,
            lastName = self.lastName,
            email = self.email,
            hashedPassword = self.hashedPassword
        )

        for c_id in self.checklist_ids:
            association = user_models.UsersChecklists(checklist_id = c_id)
            user.users_checklists.append(association)

        return user

    def _update_user(self, existing_user: user_models.User) -> user_models.User:
        existing_user.firstName = self.firstName
        existing_user.lastName = self.lastName
        existing_user.email = self.email
        existing_user.hashedPassword = self.hashedPassword

        new_checklist_ids = set(self.checklist_ids)
        existing_checklist_ids = set()
        for uc in existing_user.users_checklists:
            existing_checklist_ids.add(uc.checklist_id)

        updated_associations = []
        for uc in existing_user.users_checklists:
            if uc.checklist_id in new_checklist_ids:
                updated_associations.append(uc)

        for c_id in new_checklist_ids:
            if c_id not in existing_checklist_ids:
                association = user_models.UsersChecklists(checklist_id = c_id)
                updated_associations.append(association)

        existing_user.users_checklists = updated_associations

        return existing_user


class UserResponse(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: EmailStr
    checklist_ids: List[int] = []

    class Config:
        from_attributes = True

    @classmethod
    def orm_to_dto(cls, user: user_models.User):
        user_dto = cls.model_validate(user, from_attributes = True)

        for assoc in user.users_checklists:
            user_dto.checklist_ids.append(assoc.checklist_id)

        return user_dto
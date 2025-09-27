from typing import List, Optional
from pydantic import BaseModel
from src.checklists import models as checklist_models
from src.users import models as user_models


class Item(BaseModel):
    id: Optional[int] = None
    text: str
    isComplete: bool
    checklistId: Optional[int] = None

    def dto_to_orm(self, checklist_id: Optional[int] = None) -> checklist_models.Item:
        return checklist_models.Item(
            id = self.id,
            text = self.text,
            isComplete = self.isComplete,
            checklistId = self.checklistId or checklist_id
        )

class ItemResponse(Item):
    id: int
    checklistId: int

    class Config:
        from_attributes = True

class Checklist(BaseModel):
    id: Optional[int] = None
    title: str
    items: List[Item] = []
    user_ids: List[int] = []

    def dto_to_orm(self, checklist: Optional[checklist_models.Checklist] = None):
        if checklist is None:
            return self._create_checklist()
        return self._update_checklist(checklist)

    def _create_checklist(self) -> checklist_models.Checklist:
        checklist = checklist_models.Checklist(title = self.title)
        for item in self.items:
            checklist.items.append(item.dto_to_orm())
        for u_id in self.user_ids:
            association = user_models.UsersChecklists(user_id = u_id)
            checklist.users_checklists.append(association)
        return checklist

    def _update_checklist(self, checklist: checklist_models.Checklist) -> checklist_models.Checklist:
        checklist.title = self.title
        checklist.items = self._update_items(checklist)
        checklist.users_checklists = self._update_users(checklist)

        return checklist

    def _update_items(self, checklist: checklist_models.Checklist) -> list[checklist_models.Item]:
        existing_items = {}
        for item in checklist.items:
            existing_items[item.id] = item

        updated_items = []
        for item in self.items:
            if item.id is None:
                updated_items.append(item.dto_to_orm(checklist.id))
            elif item.id in existing_items:
                updated_item = existing_items[item.id]
                updated_item.text = item.text
                updated_item.isComplete = item.isComplete
                updated_items.append(updated_item)

        return updated_items

    def _update_users(self, checklist: checklist_models.Checklist) -> list[user_models.UsersChecklists]:
        new_user_ids = set(self.user_ids)
        existing_user_ids = set()
        for uc in checklist.users_checklists:
            existing_user_ids.add(uc.user_id)

        updated_users = []
        for uc in checklist.users_checklists:
            if uc.user_id in new_user_ids:
                updated_users.append(uc)

        for u_id in new_user_ids:
            if u_id not in existing_user_ids:
                association = user_models.UsersChecklists(user_id = u_id)
                updated_users.append(association)

        return updated_users


class ChecklistResponse(Checklist):
    id: int
    items: List[ItemResponse] = []
    user_ids: List[int] = []

    class Config:
        from_attributes = True
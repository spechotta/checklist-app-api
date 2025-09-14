from typing import List, Optional
from pydantic import BaseModel
from src.checklists import models


class Item(BaseModel):
    id: Optional[int] = None
    text: str
    isComplete: bool
    checklistId: Optional[int] = None

    def dto_to_orm(self, checklist_id: Optional[int] = None) -> models.Item:
        return models.Item(
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

    def dto_to_orm(self, checklist: Optional[models.Checklist] = None):
        if checklist is None:
            return self._create_checklist()
        return self._update_checklist(checklist)

    def _create_checklist(self) -> models.Checklist:
        checklist = models.Checklist(title = self.title)
        for item in self.items:
            checklist.items.append(item.dto_to_orm())
        return checklist

    def _update_checklist(self, checklist: models.Checklist) -> models.Checklist:
        checklist.title = self.title

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

        checklist.items = updated_items

        return checklist

class ChecklistResponse(Checklist):
    id: int
    items: List[ItemResponse] = []

    class Config:
        from_attributes = True
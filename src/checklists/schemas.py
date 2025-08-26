from typing import List, Optional
from pydantic import BaseModel
from src.checklists import models


class ItemBase(BaseModel):
    text: str
    isComplete: bool

class ItemCreate(ItemBase):
    def dto_to_orm(self) -> models.Item:
        return models.Item(
            text = self.text,
            isComplete = self.isComplete
        )

class ItemUpdate(ItemBase):
    id: Optional[int] = None

    def dto_to_orm(self) -> models.Item:
        return models.Item(
            id = self.id,
            text = self.text,
            isComplete = self.isComplete
        )

class ItemResponse(ItemBase):
    id: int
    checklistId: int

    class Config:
        from_attributes = True

class ChecklistBase(BaseModel):
    title: str

class ChecklistCreate(ChecklistBase):
    items: List[ItemCreate] = []

    def dto_to_orm(self) -> models.Checklist:
        checklist = models.Checklist(title = self.title)
        for item in self.items:
            checklist.items.append(item.dto_to_orm())
        return checklist

class ChecklistUpdate(ChecklistBase):
    id: int
    items: List[ItemUpdate] = []

    def dto_to_orm(self, checklist_id: int) -> models.Checklist:
        checklist = models.Checklist(id = checklist_id)
        checklist.title = self.title
        for item in self.items:
            checklist.items.append(item.dto_to_orm())
        return checklist

class ChecklistResponse(ChecklistBase):
    id: int
    items: List[ItemResponse] = []

    class Config:
        from_attributes = True
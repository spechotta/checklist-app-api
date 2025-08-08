from typing import List
from fastapi import APIRouter, status, Response
from src.checklists import service
from src.checklists.schemas import ChecklistResponse, ChecklistCreate, ItemCreate, ItemResponse, ItemBase
from src.dependencies import DbSession

router = APIRouter(prefix = "/checklists", tags = ["Checklists"])

@router.get("", response_model = List[ChecklistResponse])
def get_checklists(db: DbSession):
    return service.get_checklists(db)

@router.get("/{checklist_id}", response_model = ChecklistResponse)
def get_checklist(checklist_id: int, db: DbSession):
    return service.get_checklist(checklist_id, db)

@router.post("", status_code = status.HTTP_201_CREATED, response_model = ChecklistResponse)
def create_checklist(checklist: ChecklistCreate, db: DbSession):
    return service.create_checklist(checklist, db)

@router.post("/{checklist_id}/items", status_code = status.HTTP_201_CREATED, response_model = ItemResponse)
def add_item_to_checklist(checklist_id: int, item: ItemCreate, db: DbSession):
    return service.add_item_to_checklist(checklist_id, item, db)

@router.delete("/{checklist_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_checklist(checklist_id: int, db: DbSession):
    service.delete_checklist(checklist_id, db)
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.get("/{checklist_id}/items", response_model = List[ItemResponse])
def get_items(checklist_id: int, db: DbSession):
    return service.get_items(checklist_id, db)

@router.get("/{checklist_id}/items/{item_id}", response_model = ItemResponse)
def get_item(checklist_id: int, item_id: int, db: DbSession):
    return service.get_item(checklist_id, item_id, db)

@router.put("/{checklist_id}/items/{item_id}", status_code = status.HTTP_200_OK, response_model = ItemResponse)
def update_item(checklist_id: int, item_id: int, item: ItemBase, db: DbSession):
    return service.update_item(checklist_id, item_id, item, db)

@router.delete("/{checklist_id}/items/{item_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_item(checklist_id: int, item_id: int, db: DbSession):
    service.delete_item(checklist_id, item_id, db)
    return Response(status_code = status.HTTP_204_NO_CONTENT)
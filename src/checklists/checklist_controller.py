from typing import List
from fastapi import APIRouter, status, Response
from src.checklists import checklist_service
from src.checklists.checklist_schemas import Item, ItemResponse, Checklist, ChecklistResponse
from src.dependencies import DbSession

router = APIRouter(prefix = "/checklists", tags = ["Checklists"])

@router.get("", status_code = status.HTTP_200_OK, response_model = List[ChecklistResponse])
def get_checklists(db: DbSession):
    return checklist_service.get_checklists(db)

@router.post("", status_code = status.HTTP_201_CREATED, response_model = ChecklistResponse)
def create_checklist(checklist: Checklist, db: DbSession):
    return checklist_service.create_checklist(checklist, db)

@router.get("/{checklist_id}", status_code = status.HTTP_200_OK, response_model = ChecklistResponse)
def get_checklist(checklist_id: int, db: DbSession):
    return checklist_service.get_checklist(checklist_id, db)

@router.put("/{checklist_id}", status_code = status.HTTP_200_OK, response_model = ChecklistResponse)
def update_checklist(checklist_id: int, checklist: Checklist, db: DbSession):
    return checklist_service.update_checklist(checklist_id, checklist, db)

@router.delete("/{checklist_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_checklist(checklist_id: int, db: DbSession):
    checklist_service.delete_checklist(checklist_id, db)
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.post("/{checklist_id}/items", status_code = status.HTTP_201_CREATED, response_model = ItemResponse)
def add_item_to_checklist(checklist_id: int, item: Item, db: DbSession):
    return checklist_service.add_item_to_checklist(checklist_id, item, db)

@router.get("/{checklist_id}/items", status_code = status.HTTP_200_OK, response_model = List[ItemResponse])
def get_items(checklist_id: int, db: DbSession):
    return checklist_service.get_items(checklist_id, db)

@router.get("/{checklist_id}/items/{item_id}", status_code = status.HTTP_200_OK, response_model = ItemResponse)
def get_item(checklist_id: int, item_id: int, db: DbSession):
    return checklist_service.get_item(checklist_id, item_id, db)

@router.put("/{checklist_id}/items/{item_id}", status_code = status.HTTP_200_OK, response_model = ItemResponse)
def update_item(checklist_id: int, item_id: int, item: Item, db: DbSession):
    return checklist_service.update_item(checklist_id, item_id, item, db)

@router.delete("/{checklist_id}/items/{item_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_item(checklist_id: int, item_id: int, db: DbSession):
    checklist_service.delete_item(checklist_id, item_id, db)
    return Response(status_code = status.HTTP_204_NO_CONTENT)
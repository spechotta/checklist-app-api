from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class ChecklistNotFoundException(Exception):
    def __init__(self, checklist_id: int):
        self.checklist_id = checklist_id

class ItemNotFoundException(Exception):
    def __init__(self, checklist_id: int, item_id: int):
        self.checklist_id = checklist_id
        self.item_id = item_id

async def checklist_not_found_exception_handler(request: Request, exc: ChecklistNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": "Checklist not found"}
    )

async def item_not_found_exception_handler(request: Request, exc: ItemNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": "Item not found"}
    )

def register_checklist_exception_handlers(app: FastAPI):
    app.add_exception_handler(ChecklistNotFoundException, checklist_not_found_exception_handler)
    app.add_exception_handler(ItemNotFoundException, item_not_found_exception_handler)
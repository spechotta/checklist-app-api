from typing import List, Annotated

from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind = engine)

# Pydantic Schemas
class ItemBase(BaseModel):
    text: str
    isComplete: bool

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    checklistId: int

    class Config:
        from_attributes = True

class ChecklistBase(BaseModel):
    title: str

class ChecklistCreate(ChecklistBase):
    items: List[ItemCreate] = []

class ChecklistResponse(ChecklistBase):
    id: int
    items: List[ItemResponse] = []

    class Config:
        from_attributes = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Endpoints
@app.get("/checklists", response_model = List[ChecklistResponse])
async def get_checklists(db: db_dependency):
    db_checklists = db.query(models.Checklist).all()
    return db_checklists

@app.get("/checklists/{checklist_id}", response_model = ChecklistResponse)
async def get_checklist(checklist_id: int, db: db_dependency):
    db_checklist = db.query(models.Checklist).filter(models.Checklist.id == checklist_id).first()
    if not db_checklist:
        raise HTTPException(status_code = 404, detail = "Checklist not found")
    return db_checklist

@app.post("/checklists", status_code = status.HTTP_201_CREATED, response_model = ChecklistResponse)
async def create_checklist(checklist: ChecklistCreate, db: db_dependency):
    db_checklist = models.Checklist(title = checklist.title)
    db.add(db_checklist)
    db.commit()
    db.refresh(db_checklist)

    for item in checklist.items:
        db_item = models.Item(
            text = item.text,
            isComplete = item.isComplete,
            checklistId = db_checklist.id
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_checklist)
    return db_checklist

@app.put("/checklists/{checklist_id}/items", status_code = status.HTTP_200_OK, response_model = ItemResponse)
async def add_item_to_checklist(checklist_id: int, item: ItemCreate, db: db_dependency):
    db_checklist = db.query(models.Checklist).filter(models.Checklist.id == checklist_id).first()
    if not db_checklist:
        raise HTTPException(status_code = 404, detail = "Checklist not found")

    db_item = models.Item(
        text = item.text,
        isComplete = item.isComplete,
        checklistId = checklist_id
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/checklists/{checklist_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_checklist(checklist_id: int, db: db_dependency):
    db_checklist = db.query(models.Checklist).filter(models.Checklist.id == checklist_id).first()
    if not db_checklist:
        raise HTTPException(status_code = 404, detail = "Checklist not found")

    db.delete(db_checklist)
    db.commit()

@app.get("/items", response_model = List[ItemResponse])
async def get_items(db: db_dependency):
    db_items = db.query(models.Item).all()
    return db_items

@app.get("/items/{item_id}", response_model = ItemResponse)
async def get_item(item_id: int, db: db_dependency):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code = 404, detail = "Item not found")
    return db_item

@app.put("/items/{item_id}", status_code = status.HTTP_200_OK, response_model = ItemResponse)
async def update_item(item_id: int, item: ItemBase, db: db_dependency):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code = 404, detail = "Item not found")

    db_item.text = item.text
    db_item.isComplete = item.isComplete

    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: db_dependency):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code = 404, detail = "Item not found")

    db.delete(db_item)
    db.commit()
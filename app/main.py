from typing import List, Annotated
from fastapi import FastAPI, Depends, status, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app import models
from app.database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind = engine)

#CORS Middleware
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

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

@app.post("/checklists/{checklist_id}/items", status_code = status.HTTP_201_CREATED, response_model = ItemResponse)
async def add_item_to_checklist(checklist_id: int, item: ItemCreate, db: db_dependency):
    db_checklist = db.query(models.Checklist).filter(models.Checklist.id == checklist_id).first()
    if not db_checklist:
        raise HTTPException(status_code = 404, detail = "Checklist not found")

    db_item = models.Item(
        text = item.text,
        isComplete = item.isComplete,
        checklistId = checklist_id
    )
    db_checklist.items.append(db_item)

    db.commit()
    db.refresh(db_checklist)
    return db_item

@app.delete("/checklists/{checklist_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_checklist(checklist_id: int, db: db_dependency):
    db_checklist = db.query(models.Checklist).filter(models.Checklist.id == checklist_id).first()
    if not db_checklist:
        raise HTTPException(status_code = 404, detail = "Checklist not found")

    db.delete(db_checklist)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.get("/checklists/{checklist_id}/items", response_model = List[ItemResponse])
async def get_items(checklist_id: int, db: db_dependency):
    db_checklist = db.query(models.Checklist).filter(models.Checklist.id == checklist_id).first()
    if not db_checklist:
        raise HTTPException(status_code = 404, detail = "Checklist not found")

    items = db_checklist.items
    return items

@app.get("/checklists/{checklist_id}/items/{item_id}", response_model = ItemResponse)
async def get_item(checklist_id: int, item_id: int, db: db_dependency):
    db_item = (db.query(models.Item)
               .filter(models.Item.checklistId == checklist_id, models.Item.id == item_id)
               .first())

    if not db_item:
        raise HTTPException(status_code = 404, detail = "Item not found")
    return db_item

@app.put("/checklists/{checklist_id}/items/{item_id}", status_code = status.HTTP_200_OK, response_model = ItemResponse)
async def update_item(checklist_id: int, item_id: int, item: ItemBase, db: db_dependency):
    db_item = (db.query(models.Item)
               .filter(models.Item.checklistId == checklist_id, models.Item.id == item_id)
               .first())

    if not db_item:
        raise HTTPException(status_code = 404, detail = "Item not found")

    db_item.text = item.text
    db_item.isComplete = item.isComplete

    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/checklists/{checklist_id}/items/{item_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_item(checklist_id: int, item_id: int, db: db_dependency):
    db_item = (db.query(models.Item)
               .filter(models.Item.checklistId == checklist_id, models.Item.id == item_id)
               .first())

    if not db_item:
        raise HTTPException(status_code = 404, detail = "Item not found")

    db.delete(db_item)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)
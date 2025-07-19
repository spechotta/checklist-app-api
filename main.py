from typing import Annotated

from fastapi import FastAPI, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind = engine)

class ItemBase(BaseModel):
    text: str
    isComplete: bool

class Item(ItemBase):
    id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/items", status_code = status.HTTP_201_CREATED)
async def create_item(item: ItemBase, db: db_dependency):
    db_item = models.Checklist(text=item.text, isComplete = item.isComplete)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
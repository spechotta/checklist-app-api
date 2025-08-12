from sqlalchemy.orm import Session
from src.checklists import models
from src.checklists.models import Item, Checklist
from src.checklists.schemas import ChecklistCreate, ItemCreate

def get_all_checklists(db: Session):
    return db.query(models.Checklist).all()

def get_checklist_by_id(checklist_id: int, db: Session):
    return db.query(models.Checklist).filter(models.Checklist.id == checklist_id).first()

def create_checklist(checklist: ChecklistCreate, db: Session):
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

def add_item_to_checklist(db_checklist: Checklist, item: ItemCreate, db: Session):
    db_item = models.Item(
        text = item.text,
        isComplete = item.isComplete,
        checklistId = db_checklist.id
    )
    db_checklist.items.append(db_item)

    db.commit()
    db.refresh(db_item)
    return db_item

def delete_checklist(db_checklist: Checklist, db: Session):
    db.delete(db_checklist)
    db.commit()

def get_item_by_id(checklist_id: int, item_id: int, db: Session):
    return (db.query(models.Item)
            .filter(models.Item.checklistId == checklist_id, models.Item.id == item_id)
            .first())

def save_item(db_item: Item, db: Session):
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db_item: Item, db: Session):
    db.delete(db_item)
    db.commit()
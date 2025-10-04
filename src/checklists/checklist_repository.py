from sqlalchemy.orm import Session
from src.checklists import checklist_models
from src.checklists.checklist_schemas import Checklist, Item


def get_all_checklists(db: Session):
    return db.query(checklist_models.Checklist).all()

def create_checklist(checklist: Checklist, db: Session):
    db_checklist = checklist_models.Checklist(title = checklist.title)
    db.add(db_checklist)
    db.commit()
    db.refresh(db_checklist)

    for item in checklist.items:
        db_item = checklist_models.Item(
            text = item.text,
            isComplete = item.isComplete,
            checklistId = db_checklist.id
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_checklist)
    return db_checklist

def get_checklist_by_id(checklist_id: int, db: Session):
    return db.query(checklist_models.Checklist).filter(checklist_models.Checklist.id == checklist_id).first()

def save_checklist(db_checklist: Checklist, db: Session):
    db.commit()
    db.refresh(db_checklist)
    return db_checklist

def delete_checklist(db_checklist: Checklist, db: Session):
    db.delete(db_checklist)
    db.commit()

def add_item_to_checklist(db_checklist: Checklist, item: Item, db: Session):
    db_item = checklist_models.Item(
        text = item.text,
        isComplete = item.isComplete,
        checklistId = db_checklist.id
    )
    db_checklist.items.append(db_item)

    db.commit()
    db.refresh(db_item)
    return db_item

def get_item_by_id(checklist_id: int, item_id: int, db: Session):
    return (db.query(checklist_models.Item)
            .filter(checklist_models.Item.checklistId == checklist_id, checklist_models.Item.id == item_id)
            .first())

def save_item(db_item: Item, db: Session):
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db_item: Item, db: Session):
    db.delete(db_item)
    db.commit()
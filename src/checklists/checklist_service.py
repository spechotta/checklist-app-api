from sqlalchemy.orm import Session
from src.checklists import checklist_repository
from src.checklists.checklist_exceptions import ChecklistNotFoundException, ItemNotFoundException
from src.checklists.checklist_schemas import Item, Checklist


def get_checklists(db: Session):
    return checklist_repository.get_all_checklists(db)

def create_checklist(checklist_create: Checklist, db: Session):
    db_checklist = checklist_create.dto_to_orm()
    return checklist_repository.create_checklist(db_checklist, db)

def get_checklist(checklist_id: int, db: Session):
    db_checklist = checklist_repository.get_checklist_by_id(checklist_id, db)
    if not db_checklist:
        raise ChecklistNotFoundException(checklist_id)
    return db_checklist

def update_checklist(checklist_id: int, checklist_update: Checklist, db: Session):
    db_checklist = checklist_repository.get_checklist_by_id(checklist_id, db)
    if not db_checklist:
        raise ChecklistNotFoundException(checklist_id)

    checklist_update.dto_to_orm(db_checklist)
    return checklist_repository.save_checklist(db_checklist, db)

def delete_checklist(checklist_id: int, db: Session):
    db_checklist = checklist_repository.get_checklist_by_id(checklist_id, db)
    if not db_checklist:
        raise ChecklistNotFoundException(checklist_id)
    checklist_repository.delete_checklist(db_checklist, db)

def add_item_to_checklist(checklist_id: int, item: Item, db: Session):
    db_checklist = checklist_repository.get_checklist_by_id(checklist_id, db)
    if not db_checklist:
        raise ChecklistNotFoundException(checklist_id)
    return checklist_repository.add_item_to_checklist(db_checklist, item, db)

def get_items(checklist_id: int, db: Session):
    db_checklist = checklist_repository.get_checklist_by_id(checklist_id, db)
    if not db_checklist:
        raise ChecklistNotFoundException(checklist_id)
    return db_checklist.items

def get_item(checklist_id: int, item_id: int, db: Session):
    db_item = checklist_repository.get_item_by_id(checklist_id, item_id, db)
    if not db_item:
        raise ItemNotFoundException(checklist_id, item_id)
    return db_item

def update_item(checklist_id: int, item_id: int, item: Item, db: Session):
    db_item = checklist_repository.get_item_by_id(checklist_id, item_id, db)
    if not db_item:
        raise ItemNotFoundException(checklist_id, item_id)

    db_item.text = item.text
    db_item.isComplete = item.isComplete

    return checklist_repository.save_item(db_item, db)

def delete_item(checklist_id: int, item_id: int, db: Session):
    db_item = checklist_repository.get_item_by_id(checklist_id, item_id, db)
    if not db_item:
        raise ItemNotFoundException(checklist_id, item_id)
    checklist_repository.delete_item(db_item, db)
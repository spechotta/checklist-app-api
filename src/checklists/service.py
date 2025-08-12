from sqlalchemy.orm import Session
from src.checklists import repository
from src.checklists.exceptions import ChecklistNotFoundException, ItemNotFoundException
from src.checklists.schemas import ChecklistCreate, ItemCreate, ItemBase

def get_checklists(db: Session):
    return repository.get_all_checklists(db)

def get_checklist(checklist_id: int, db: Session):
    db_checklist = repository.get_checklist_by_id(checklist_id, db)
    if not db_checklist:
        raise ChecklistNotFoundException(checklist_id)
    return db_checklist

def create_checklist(checklist: ChecklistCreate, db: Session):
    return repository.create_checklist(checklist, db)

def add_item_to_checklist(checklist_id: int, item: ItemCreate, db: Session):
    db_checklist = repository.get_checklist_by_id(checklist_id, db)
    if not db_checklist:
        raise ChecklistNotFoundException(checklist_id)
    return repository.add_item_to_checklist(db_checklist, item, db)

def delete_checklist(checklist_id: int, db: Session):
    db_checklist = repository.get_checklist_by_id(checklist_id, db)
    if not db_checklist:
        raise ChecklistNotFoundException(checklist_id)
    repository.delete_checklist(db_checklist, db)

def get_items(checklist_id: int, db: Session):
    db_checklist = repository.get_checklist_by_id(checklist_id, db)
    if not db_checklist:
        raise ChecklistNotFoundException(checklist_id)
    return db_checklist.items

def get_item(checklist_id: int, item_id: int, db: Session):
    db_item = repository.get_item_by_id(checklist_id, item_id, db)
    if not db_item:
        raise ItemNotFoundException(checklist_id, item_id)
    return db_item

def update_item(checklist_id: int, item_id: int, item: ItemBase, db: Session):
    db_item = repository.get_item_by_id(checklist_id, item_id, db)
    if not db_item:
        raise ItemNotFoundException(checklist_id, item_id)

    db_item.text = item.text
    db_item.isComplete = item.isComplete

    return repository.save_item(db_item, db)

def delete_item(checklist_id: int, item_id: int, db: Session):
    db_item = repository.get_item_by_id(checklist_id, item_id, db)
    if not db_item:
        raise ItemNotFoundException(checklist_id, item_id)
    repository.delete_item(db_item, db)
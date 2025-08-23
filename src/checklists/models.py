from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key = True, index = True)
    text = Column(String(200), nullable = False)
    isComplete = Column(Boolean, default = False, nullable = False)
    checklistId = Column(Integer, ForeignKey("checklists.id"), nullable = False)

    checklist = relationship("Checklist", back_populates = "items")

class Checklist(Base):
    __tablename__ = "checklists"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String(50), nullable = False)

    items = relationship("Item", back_populates = "checklist", cascade = "all, delete-orphan")
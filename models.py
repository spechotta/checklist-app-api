from sqlalchemy import Column, String, Boolean, Integer
from database import Base

class Checklist(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key = True, index = True)
    text = Column(String(200))
    isComplete = Column(Boolean)

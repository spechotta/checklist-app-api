from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    firstName = Column(String(50), nullable = False)
    lastName = Column(String(50), nullable = False)
    email = Column(String(100), unique = True, nullable = False, index = True)
    hashedPassword = Column(String(200), nullable = False)

    users_checklists = relationship("UsersChecklists", back_populates = "user", cascade = "all, delete-orphan")


class UsersChecklists(Base):
    __tablename__ = "users_checklists"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key = True)
    checklist_id = Column(Integer, ForeignKey("checklists.id"), primary_key = True)

    user = relationship("User", back_populates = "users_checklists")
    checklist = relationship("Checklist", back_populates = "users_checklists")
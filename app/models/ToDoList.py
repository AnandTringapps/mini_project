from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    todolists = relationship("TodoList", back_populates="owner")

class TodoList(Base):
    __tablename__ = "todolists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="todolists")
    tasks = relationship("Task", back_populates="todolist")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    due_date = Column(Date)
    status = Column(String)
    todolist_id = Column(Integer, ForeignKey("todolists.id"))

    todolist = relationship("TodoList", back_populates="tasks")

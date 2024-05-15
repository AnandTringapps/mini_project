from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    hashed_password: str

class TodoListBase(BaseModel):
    name: str
    owner_id: int

class TodoListCreate(TodoListBase):
    pass

class TodoListUpdate(BaseModel):
    name: Optional[str] = None

class TaskBase(BaseModel):
    description: str
    due_date: str
    status: str

class TaskCreate(TaskBase):
    pass

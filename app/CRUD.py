from sqlalchemy.orm import Session
from models import ToDoList
import schemas

def get_user_by_email(db: Session, email: str):
    return db.query(ToDoList.User).filter(ToDoList.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = ToDoList.User(username=user.username, email=user.email, hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_todo_list(db: Session, todolist_id: int):
    return db.query(ToDoList.TodoList).filter(ToDoList.TodoList.id == todolist_id).first()

def create_todolist(db: Session, todo_list: schemas.TodoListCreate):
    db_todolist = ToDoList.TodoList(name=todo_list.name, owner_id=todo_list.owner_id)
    db.add(db_todolist)
    db.commit()
    db.refresh(db_todolist)
    return db_todolist

def get_all_todolists(db: Session):
    return db.query(ToDoList.TodoList).all()

def update_todolist(db: Session, todolist_id: int, updated_todolist: schemas.TodoListUpdate):
    db_todolist = db.query(ToDoList.TodoList).filter(ToDoList.TodoList.id == todolist_id).first()
    if db_todolist:
        for attr, value in updated_todolist.dict().items():
            setattr(db_todolist, attr, value)
        db.commit()
        db.refresh(db_todolist)
        return db_todolist
    else:
        return None

def delete_todolist(db: Session, todolist_id: int):
    db_todolist = db.query(ToDoList.TodoList).filter(ToDoList.TodoList.id == todolist_id).first()
    if db_todolist:
        db.delete(db_todolist)
        db.commit()
        return db_todolist
    else:
        return None

def create_task(db: Session, todolist_id: int, task: ToDoList.TaskCreate):
    db_task = ToDoList.Task(**task.dict(), todolist_id=todolist_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_all_tasks(db: Session, todolist_id: int):
    return db.query(ToDoList.Task).filter(ToDoList.Task.todolist_id == todolist_id).all()

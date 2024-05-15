from fastapi import FastAPI, Request, Depends, Form, status, HTTPException
from fastapi.templating import Jinja2Templates
from models.ToDoList import Task as Todo, User
from database.database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError
from database.database import CLIENT_ID, CLIENT_SECRET
from fastapi.staticfiles import StaticFiles
from schemas import UserCreate

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.add_middleware(SessionMiddleware, secret_key="add any string...")

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_url': 'http://localhost:8000/auth'
    }
)

@app.get("/")
def index(request: Request):
    user = request.session.get('user')
    if user:
        return RedirectResponse('welcome')

    return templates.TemplateResponse(
        name="home.html",
        context={"request": request}
    )


@app.get('/welcome')
def welcome(request: Request):
    user = request.session.get('user')
    if not user:
        return RedirectResponse('/')
    return templates.TemplateResponse(
        name='welcome.html',
        context={'request': request, 'user': user}
    )


@app.get("/login")
async def login(request: Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)


@app.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return templates.TemplateResponse(
            name='error.html',
            context={'request': request, 'error': e.error}
        )
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse('base')
@app.post("/user/create")
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(**user_data.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get('/logout')
def logout(request: Request):
    request.session.pop('user')
    request.session.clear()
    return RedirectResponse('/')

@app.get("/todo")
async def home(request: Request, db: Session = Depends(get_db)):
    user = request.session.get('user')
    if user:
        todos = db.query(Todo).order_by(Todo.id.desc())
        return templates.TemplateResponse("todo.html", {"request": request, "todos": todos})
    else:
        return RedirectResponse('/login')

@app.post("/todo/add")
async def add(request: Request, task: str = Form(...), db: Session = Depends(get_db)):
    user = request.session.get('user')
    if user:
        todo = Todo(task=task)
        db.add(todo)
        db.commit()
        return RedirectResponse(url="/todo", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse('/login')

@app.get("/todo/edit/{todo_id}")
async def edit(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = request.session.get('user')
    if user:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        return templates.TemplateResponse("todo.html", {"request": request, "todo": todo})
    else:
        return RedirectResponse('/login')

@app.post("/todo/edit/{todo_id}")
async def edit(request: Request, todo_id: int, task: str = Form(...), completed: bool = Form(False), db: Session = Depends(get_db)):
    user = request.session.get('user')
    if user:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        todo.task = task
        todo.completed = completed
        db.commit()
        return RedirectResponse(url="/todo", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse('/login')

@app.get("/todo/delete/{todo_id}")
async def delete(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = request.session.get('user')
    if user:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        db.delete(todo)
        db.commit()
        return RedirectResponse(url="/todo", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse('/login')
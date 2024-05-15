from fastapi import FastAPI
from routes.ToDoList import app
from database.database import Base, engine

router = FastAPI()

Base.metadata.create_all(bind=engine)
print("Table created")

router.include_router(app.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

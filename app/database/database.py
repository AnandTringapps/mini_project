from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData


DATABASE_URL='postgresql://postgres:123@localhost:5432/ToDoList'

engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0,
                       echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


metadata = MetaData()

metadata.reflect(bind=engine)

if 'users' in metadata.tables and 'todolists' in metadata.tables and 'tasks' in metadata.tables and 'todos' in metadata.tables:
    print("All tables exist in the database.")
else:
    print("One or more tables are missing from the database.")



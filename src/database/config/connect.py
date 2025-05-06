import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

PASSWORD = os.getenv('PASSWORD')
USER = os.getenv('USER')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')
HOST = os.getenv('HOST')
DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

engine = create_engine(
    DATABASE_URL, 
    connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def create_db():
    Base.metadata.create_all(bind=engine)
       
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close          
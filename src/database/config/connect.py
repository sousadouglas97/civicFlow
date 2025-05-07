import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

load_dotenv()

PASSWORD = os.getenv('PASSWORD')
USER = os.getenv('USER')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')
HOST = os.getenv('HOST')

DATABASE_URL = f'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
engine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_database():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
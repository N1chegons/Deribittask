from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from src.config import settings


class Base(DeclarativeBase):
    pass

DB_URL = settings.DB_URL

sync_engine = create_engine(DB_URL)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


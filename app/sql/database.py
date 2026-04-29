from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

from app.logs.config import BASE_DIR
SQL_DIR = BASE_DIR / "app" / "sql"
engine = create_engine(f'sqlite:///{SQL_DIR / "db-sqlite.db"}')

class Base(DeclarativeBase):
    pass

Sess = sessionmaker(bind=engine)
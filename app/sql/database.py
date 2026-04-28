from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

# import os

# Depends in the database that you're using
# db_user = os.getenv("POSTGRES_USER")
# db_pass = os.getenv("POSTGRES_PASSWORD")
# db_name = os.getenv("POSTGRES_DB")

engine = create_engine(f'sqlite:///db-sqlite.db')

class Base(DeclarativeBase):
    pass

AutoBase = automap_base()
AutoBase.prepare(autoload_with=engine)

SessionLocal = sessionmaker(bind=engine)

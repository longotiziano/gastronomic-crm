from app.models.raw_material import RawMaterial
from app.models.stock import Stock
from app.repositories.base_repository import Repository
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
import pandas as pd
from typing import Literal
    
from app.logs.loggers import start_logger
logger = start_logger(__name__)

class RawMaterialRepository(Repository[RawMaterial]):
    """
    Contains the interactions related to the raw material's tables
    """
    def __init__(self, session):
        super().__init__(session, RawMaterial, "rm_name", "rm_id")
    
    
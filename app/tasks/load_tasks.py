from app.repositories.raw_material_repository import RawMaterialRepository

from sql.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from typing import Literal, Any

from logs.loggers import start_logger
logger = start_logger(__name__)

def load_data_task(
    df: pd.DataFrame,
    table: Any, 
    direction: Literal['stock_in', 'stock_out']
) -> tuple[bool, str]:
    """
    General function to update the database with a table
    ### Receives:
    - DataFrame
    - The table's class
    - Direction of the stock movement
    ### Returns:
    - Boolean value
    - Error message
    """
    with SessionLocal() as session:
        rm_repo = RawMaterialRepository(session)
        r_id = df['r_id'].iloc[0]

        update_ok, er = rm_repo.update_stock_amounts(r_id, df, direction)
        if not update_ok:
            return False, er
        
        list_of_dicts = df.to_dict(orient='records')
        try:
            session.bulk_insert_mappings(table, list_of_dicts) # type: ignore

        except SQLAlchemyError as e:
            er = f"Unexpected error ocurred while finding stock's amounts -> Error: {e}"
            logger.error(er)
            return False, er
        
        session.commit()    

    return True, ""

def load_stock_movements_task(directory_parameter):
    from app.models.auto_models import StockMovements

    ok, error = load_data_task(directory_parameter, StockMovements)
    if not ok:
        raise error

def load_sales_task(directory_parameter):
    from app.models.auto_models import Sales

    ok, error = load_data_task(directory_parameter, Sales)
    if not ok:
        raise error

    
        
            
            
    
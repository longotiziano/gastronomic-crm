from app.models.auto_models import RawMaterial, Stock
from app.repositories.base_repository import Repository
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
import pandas as pd
from typing import Literal
    
from logs.loggers import start_logger
logger = start_logger(__name__)

class RawMaterialRepository(Repository):
    """
    Contains the interactions related to the raw material's tables
    """
    model = RawMaterial
    name = 'rm_name'
    id = 'rm_id'
    
    def _rm_df_to_dict(self, df: pd.DataFrame) -> dict[str, float]:
        '''
        Construye el diccionario que funciona para actualizar la base de datos
        '''
        return dict(zip(df['rm_name'], df['amount']))

    def _get_all_rm_amounts(self, r_id: int) -> dict[str, float]:
        """
        ### Receives:
        - r_id
        ### Returns:
        - A dictionary of raw material and it's stored amount for the selected restaurant
        """
        results = self.session.query(
            RawMaterial.rm_name,
            Stock.stock_amount
        ).join(
            RawMaterial, RawMaterial.rm_id == Stock.rm_id
        ).filter(
            RawMaterial.r_id == r_id
        ).all()
        
        results_dict = dict(results)
        logger.debug("Extracted raw material and it's stored amount -> Records' amount: %s", len(results_dict))
        return results_dict

    def update_stock_amounts(
        self, 
        r_id: int,  
        df: pd.DataFrame,   
        direction: Literal["stock_in", "stock_out"] = "stock_in"
        ) -> tuple[bool, str]:
        '''
        Actualizando las cantidades de stock basadas en un DataFrame
        ''' 
        # Construyendo el diccionario
        rm_dict = self._rm_df_to_dict(df)

        # Grabbing the stock for each raw material
        try:    
            stocks = (
                self.session.query(Stock)
                .join(RawMaterial, Stock.rm_id == RawMaterial.rm_id)
                .filter(
                    RawMaterial.r_id == int(r_id),
                    RawMaterial.rm_name.in_(rm_dict.keys())
                )
                .options(joinedload(Stock.raw_material)) # keeping the table in the variable
                .all()
            )
        except SQLAlchemyError as e:
            er = f"Unexpected error ocurred while finding stock's amounts -> Error: {e}"
            logger.error(er)
            return False, er

        for stock in stocks:
            rm_name = stock.raw_material.rm_name
            amount = rm_dict.get(rm_name, 0)
            if direction == "stock_out":
                amount = -amount
            stock.stock_amount = float(stock.stock_amount) + amount
        
        return True, ""

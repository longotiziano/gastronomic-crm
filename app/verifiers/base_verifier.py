from app.repositories.raw_material_repository import RawMaterialRepository

from sqlalchemy import inspect

from typing import Generic, TypeVar
T = TypeVar('T')

from app.logs.loggers import start_logger
logger = start_logger(__name__)

class Verifier(Generic[T]):
    def __init__(self, model):
        self.model = model

    def _obtain_required_cols(self):
        _mapper = inspect(self.model)
        return [name for name, col in _mapper.columns.items() if not col.nullable]

class VerifyExistence(Verifier):
    def verify_existence_from_df(self, r_id: int, df: pd.DataFrame) -> tuple[bool, None | list]:
        '''
        Verificando elementos solo para DataFrames
        '''
        existing_values = self._get_existing_values(r_id)
        errors = []
        for row in df.itertuples():
            value = getattr(row, self.name)    
            if value not in existing_values:
                errors.append(value)
        
        if errors:
            return False, errors
        
        return True, None
    
    def verify_existence(self, r_id: int, value: str) -> tuple[bool, None | str]:
        '''
        Verificando valores singulares por su existencia en al base de datos
        '''
        existing_values = self._get_existing_values(r_id)

        if value not in existing_values:
            return False, value
        return True, None
    
class StockAmountVerifier(Verifier):
    def verify_negative_amounts_from_df(self, df: pd.DataFrame) -> tuple[bool, dict]:
        """
        Receives:
        - A dataframe (depends on the children)
        Returns:
        - A boolean value
        - A dictionary of the records with negative amounts
        """
        negative_amounts = df[df["amount"] < 0]

        if not negative_amounts.empty:
            negative_amounts_dict = negative_amounts.set_index(self.name).to_dict()['amount']
            
            for name, amount in negative_amounts_dict.items():
                 logger.warning("Negative amount detected -> %s: %s | Amount: %s", self.name, name, amount)

            return False, negative_amounts_dict
        
        logger.debug("Succesfully verified all negative amounts in dataframe")
        return True, {}
            
        
    def verify_amount_from_df(self, r_id: int, df: pd.DataFrame) -> tuple[bool, dict]:
        '''
        ### Receives:
        - r_id
        - A dataframe (raw material or products)
        ### Returns:
        - A boolean value
        - A dictionary of the amounts that surpasses the stored amount
        '''
        repository = RawMaterialRepository(self.session)
        rm_amounts_dict = repository._get_all_rm_amounts(r_id)
        
        surpassed_amounts = df[df["amount"] > rm_amounts_dict[self.name]] # self.name would be "rm_name"
        
        if not surpassed_amounts.empty:
            surpassed_amounts_dict = surpassed_amounts.set_index(self.name).to_dict()['amount']
            
            for name, amount in surpassed_amounts_dict.items():
                comparison = f"{rm_amounts_dict[self.name]} < {amount}"
                logger.warning("Inserted amount surpasses the stored one -> Raw material name: %s | Stored vs Inserted: %s", name, comparison)

            return False, surpassed_amounts_dict
        
        logger.debug("Succesfully verified all raw material amounts in dataframe -> r_id: %s", r_id)
        return True, {}
from app.verifiers.base_verifier import Verifier
from sql.database import SessionLocal

import pandas as pd
from typing import Literal, Optional, Any, Callable

from logs.loggers import start_logger
logger = start_logger(__name__)

def verify_task(
    verifier_class: Any,
    df: pd.DataFrame,
    method_name: str,
    direction: Optional[Literal['stock_in', 'stock_out']] = None
) -> tuple[bool, str]: 
    '''
    Verifies the inserted records matching them with the database, negative values and that the received amount isn't bigger the stored one. 
    In case that the verification is on the products, the last mention doesn't apply. 
    ### Receives:
    - The class of the object that you want to verify
    - DataFrame
    - A string with the verification method
    - The direction of the movement (in case of raw material)
    ### Returns:
    - Bool
    - String error
    '''  
    with SessionLocal() as session:
        verifier: Verifier = verifier_class(session)
        r_id = df['r_id'].iloc[0]
        verifier_method: Callable = getattr(verifier, method_name)
        # Teniendo en cuenta que ProductDfVerifier no tiene un parámetro "direction", aplico esta estrategia
        if direction:
            ok, error_dict = verifier_method(r_id, df, direction)
        else:
            ok, error_dict = verifier_method(r_id, df)
        if not ok:
            # Already logged
            er = f"Unexpected error ocurred while verifying input data -> Error: {error_dict}"
            return False, er
    return True, ""
    
def verify_rm_task(
    directory_provided, 
    direction: Literal['stock_in', 'stock_out']
) -> tuple[bool, str]:
    from app.verifiers.raw_material_verifiers import RawMaterialDfVerifier
    ok, er = verify_task(RawMaterialDfVerifier, directory_provided, 'rm_df_verifier', direction)
    if not ok:
        return False, er
    return True, ""
    
def verify_products(directory_provided) -> tuple[bool, str]:
    from app.verifiers.products_verifiers import ProductDfVerifier
    ok, er = verify_task(ProductDfVerifier, directory_provided, 'products_df_verifier')
    if not ok:
        return False, er
    return True, ""  










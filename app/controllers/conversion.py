from app.models.auto_models import RawMaterial, Products, Recipes
from app.repositories.products_repository import ProductsRepository
from app.repositories.raw_material_repository import RawMaterialRepository
from app.repositories.base_repository import Repository
import pandas as pd
from typing import Literal
from collections import defaultdict
from sqlalchemy.orm import Session

def products_to_raw_material_df(r_id: int, df: pd.DataFrame, session: Session) -> pd.DataFrame:
    '''
    ### Receives:
    - r_id
    - Products' dataframe
    - SQL session
    ### Returns:
    - A dataframe with the consumed raw material
    '''
    product_names = df['product_name'].tolist()
    repository = Repository(session)
    recipes = repository._get_recipes_by_products(r_id, product_names, session)

    raw_material_amounts = defaultdict(float)
    for product_name, rm_name, rm_amount in recipes:
        amount = df.loc[df['product_name'] == product_name, 'amount'].iloc[0]
        raw_material_amounts[rm_name] += float(rm_amount) * amount

    return pd.DataFrame([
        {'r_id': r_id, 'rm_name': k, 'amount': v}
        for k, v in raw_material_amounts.items()
    ])
    
def products_df_to_sales(r_id: int, df: pd.DataFrame, session: Session) -> tuple[bool, pd.DataFrame | list]:
    '''
    Dado un DataFrame de productos, devuelve una lista de diccionarios de ventas, con la ID de producto compaginada con su nombre
    '''
    # Obteniendo todos los IDs con una consulta
    repo = ProductsRepository(session)
    ok, product_map = repo.obtain_name_id_dict(r_id)
    # Manejando los posibles errores de la DB, con raw_material_map como posibilidad
    if not ok:
        return False, product_map
    
    list_of_dicts = []
    for row in df.itertuples():
        # Obteniendo los IDs de las coincidencias
        product_id = product_map.get(row.product_name)
        sales_dict = {
            'r_id': r_id,
            'product_id': product_id,
            'sale_quantity': row.amount
        }

        list_of_dicts.append(sales_dict)

    return True, pd.DataFrame(list_of_dicts)


def raw_material_to_stock_movements(
    r_id: int,  
    df: pd.DataFrame, 
    session: Session,
    direction: Literal["stock_in", "stock_out"] = "stock_in"
    ) -> tuple[bool, pd.DataFrame | list]:
    '''
    Dado un DataFrame de materia prima, devuelve una lista de diccionarios de movimientos de stock, con la ID de materia prima y la dirección
    del movimientos
    '''
    # Obteniendo todos los IDs con una consulta
    repo = RawMaterialRepository(session)
    ok, raw_material_map = repo.obtain_name_id_dict(r_id)
    # Manejando los posibles errores de la DB, con raw_material_map como posibilidad
    if not ok:
        return False, raw_material_map
    
    list_of_dicts = []
    for row in df.itertuples():
        # Obteniendo los IDs de las coincidencias
        rm_id = raw_material_map.get(row.rm_name)
        stock_movement_dict = {
            'r_id' : r_id,
            'rm_id' : rm_id,
            'movement_amount' : row.amount,
            'movement_type' : direction
        }
        
        list_of_dicts.append(stock_movement_dict)

    return True, pd.DataFrame(list_of_dicts)
        
        
        

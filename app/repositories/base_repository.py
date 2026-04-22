from app.models.restaurant import Restaurant
from app.models.auto_models import RawMaterial, Products, Recipes
from sqlalchemy.orm import Session

from logs.loggers import start_logger
logger = start_logger(__name__)

class Repository():
    """
    Main repository. Contains common methods and attributes that share both products and raw materials repositories.

    The attributes 'model', 'name' and 'id' are crucial. They are going to be replaced for each repository for it's columns' name.
    """
    model = None
    name: str = ""
    id: str = ""
    
    def __init__(self, session):
        self.session = session
    
    def obtain_name_id_dict(self, r_id: int) -> tuple[bool, dict]:
        '''
        Función dinámica que retorna un diccionario {'name':id} para mejor inserción en los diferentes
        repositorios con una única consulta
        '''
        results = self.session.query(
            getattr(self.model, self.name), # Columna del nombre del producto/materia prima
            getattr(self.model, self.id) # " " id " "
        ).filter(
            getattr(self.model, 'r_id') == int(r_id)
        ).all()
        
        if not results:
            logger.warning("Coulnd't find any results -> r_id: %s", r_id)
            return False, {"r_id": r_id}

        dict_results = dict(results)

        logger.debug("Dict created and returned -> r_id: %s | Records' amount: %s", r_id, len(dict_results))
        return True, dict_results
    
    def _get_recipes_by_products(self, r_id: int, product_names: list, session: Session) -> list[tuple[str, str, float]]:
        '''
        ### Receives:
        - r_id
        - A list of products
        - The SQL session
        ### Returns:
        - List of tuples, each tuple represents a record of the recipe's filtered table
        '''
        recipes = session.query(Products.product_name, RawMaterial.rm_name, Recipes.rm_amount)\
            .join(RawMaterial, RawMaterial.rm_id == Recipes.rm_id)\
            .join(Products, Products.product_id == Recipes.product_id)\
            .filter(
                Recipes.r_id == int(r_id),
                Products.product_name.in_(product_names)
            )\
            .all()
            
        logger.debug("Obtained all the recipes for the products inserted -> Products' amount: %s", len(product_names))
        return recipes

    def _get_restaurants(self) -> list:
        '''
        Devuelve una lista de los IDs de los restaurantes registrados en la DB
        '''
        restaurants_list = [r[0] for r in self.session.query(Restaurant.r_id).filter(Restaurant.r_id != -9999).all()]
        #if not restaurants_list:
        #    logger.error("Couldn't find any records in the restaurants' table")
        #    return False, []
        
        logger.debug("Finded restaurants' list -> Records' amount: %s", len(restaurants_list))
        return restaurants_list

    



from app.models.raw_material import RawMaterial
from app.models.product import Product
from app.models.recipe import Recipe
from sqlalchemy.exc import SQLAlchemyError

from app.logs.loggers import start_logger, raise_and_log
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
    
    def _count_records(self, name_looked: str = "") -> int:
        """
        ### Receives:
        - A name
        ### Returns:
        - The amounts of records that match the received name
        """
        try:
            records = self.session.query(model).filter(model.name.ilike(f"%{name_looked}%")).count()
        except SQLAlchemyError as e:
            raise_and_log("Unexpected server error during the products' records extraction", e, logger)
        return records

    def _get_records(
        self, 
        r_id: int, 
        actual_offset: int = 0, 
        page_size: int = 10, 
        name_looked: str = ""
    ) -> list[model]:
        """
        Returns a list of tuples based on an offset and page size.
        ### Receives:
        - Offset
        - Name looked
        ### Returns:
        - List of objects of the selected model
        """
        try:
            results: list[model] = self.session.query(model)\
                        .filter(model.name.ilike(f"%{name_looked}%"))\
                        .filter(model.r_id == r_id)\
                        .offset(actual_offset)\
                        .limit(page_size)\
                        .all()
        except SQLAlchemyError as e:
            raise_and_log("Unexpected server error during the records extraction", e, logger)
        if not results:
            logger.warning("Couldn't find any results while looking for records that match '%s'", name_looked)
            return [{}]
        return results
    
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
    
    def _get_recipes_by_products(self, r_id: int, product_names: list) -> list[tuple[str, str, float]]:
        '''
        ### Receives:
        - r_id
        - A list of products
        ### Returns:
        - List of tuples, each tuple represents a record of the recipe's filtered table
        '''
        try:
            recipes = self.session.query(Product.product_name, RawMaterial.rm_name, Recipe.rm_amount)\
                .join(RawMaterial, RawMaterial.rm_id == Recipe.rm_id)\
                .join(Product, Product.product_id == Recipe.product_id)\
                .filter(
                    Recipe.r_id == int(r_id),
                    Product.product_name.in_(product_names)
                )\
                .all()
        except SQLAlchemyError as e:
            raise_and_log("Unexpected server error while obtaining products' recipes", e, logger)
        if not recipes:
            raise_and_log(f"Couldn't find any recipes while looking for products that match '{product_names}'", ValueError(), logger)
            
        logger.debug("Obtained all the recipes for the products inserted -> Products' amount: %s", len(product_names))
        return recipes

    



from app.models.raw_material import RawMaterial
from app.models.product import Product
from app.models.recipe import Recipe
from sqlalchemy.exc import SQLAlchemyError

from app.logs.loggers import start_logger, raise_and_log
logger = start_logger(__name__)

from typing import TypeVar
T = TypeVar('T')

class Repository():
    """
    Main repository. Contains common methods and attributes that share both products and raw materials repositories.

    The attributes 'model', 'name' and 'id' are crucial. They are going to be replaced for each repository for it's columns' name.
    """
    def __init__(self, session, model, name, id):
        self.session = session
        self.model = model
        self.name = name
        self.id = id
        
    def _build_filtered_query(self, **filters):
        """
        Builds a query based on the parameters received
        - Parameters structure: <column_name>=<condition>
        """
        query = self.session.query(self.model)
        
        for key, value in filters.items():
            if value is not None and value != "":
                column = getattr(self.model, key, None)
                if column is not None:
                    if hasattr(column.type, 'python_type') and column.type.python_type is str:
                        query = query.filter(column.ilike(f"%{value}%"))
                    else:
                        query = query.filter(column == value)
        return query

    def _count_records(self, **kwargs) -> int:
        """
        Counts the records that match the conditions
        - Parameters structure: <column_name>=<condition>
        """
        try:
            query = self._build_filtered_query(**kwargs)
            return query.count()
        except SQLAlchemyError as e:
            raise_and_log("Error al contar registros", e, logger)

    def _get_records(self, **kwargs) -> list[T]:
        """
        Returns a list of the actual object that match the conditions
        - Parameters structure: column_name=condition
        - Pagination: actual_offset=int, page_size=int
        """
        try:
            offset = int(kwargs.pop('actual_offset', 0))
            limit = int(kwargs.pop('page_size', 10))
            query = self._build_filtered_query(**kwargs)
            return query.offset(offset).limit(limit).all()
        
        except SQLAlchemyError as e:
            raise_and_log("Error al extraer registros", e, logger)
    
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

    



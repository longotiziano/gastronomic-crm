from app.exceptions.internal_errors import InternalServerException
from app.exceptions.user_errors import DuplicateRecordException
from app.models import restaurant
from app.models import restaurant
from app.models.raw_material import RawMaterial
from app.models.product import Product
from app.models.recipe import Recipe
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


from app.utils.helpers import upload_image
from typing import Generic, TypeVar
T = TypeVar('T')

from app.logs.loggers import start_logger
logger = start_logger(__name__)

class Repository(Generic[T]):
    """
    Main repository. Contains common methods and attributes that share both products and raw materials repositories.

    The attributes 'model', 'name' and 'id' are crucial. They are going to be replaced for each repository for it's columns' name.
    """
    def __init__(self, session: Session, model, name, id):
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
        logger.debug("Building filtered query -> Filters: %s | Table: %s", filters, self.model.__tablename__)
        for key, value in filters.items():
            logger.debug("Filtering by -> %s: %s | Table: %s", key, value, self.model.__tablename__)
            if value is not None and value != "":
                column = getattr(self.model, key, None)
                if column is not None:
                    # Looks if the data type is a Python's string
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
            raise InternalServerException(detail=str(e))

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
            raise InternalServerException(detail=str(e))

    def create_record(self, **kwargs) -> T:
        """
        Creates a record with the data received and returns the created object
        - Parameters structure: column_name=value
        """
        image = kwargs.pop('image_url', None)

        if self._get_records(**kwargs):
            raise DuplicateRecordException(self.model.__table__, self.model)

        url = upload_image(image) if image else None

        try:
            new_shi = self.model(**kwargs, image_url=url)
            self.session.add(new_shi)
            self.session.commit()
            self.session.refresh(new_shi)
        except SQLAlchemyError as e:
            raise InternalServerException(str(e))

        return new_shi

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
            raise InternalServerException(detail=str(e))
        if not recipes:
            raise InternalServerException(detail=f"Couldn't find any recipes while looking for products that match '{product_names}'")
            
        logger.debug("Obtained all the recipes for the products inserted -> Products' amount: %s", len(product_names))
        return recipes

    



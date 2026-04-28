from app.models.product import Product
from app.repositories.base_repository import Repository

from sqlalchemy.exc import SQLAlchemyError

from app.logs.loggers import start_logger, raise_and_log
logger = start_logger(__name__)

class ProductsRepository(Repository):
    model = Product
    name = 'product_name'
    id = 'product_id'

    def _count_records(self, name_looked: str = "") -> int:
        """
        ### Receives:
        - A name
        ### Returns:
        - The amounts of records that match the received name
        """
        try:
            records = self.session.query(Product).filter(Product.product_name.ilike(f"%{name_looked}%")).count()
        except SQLAlchemyError as e:
            raise_and_log("Unexpected server error during the products' records extraction", e, logger)
        return records

    def get_products(self, r_id: int, actual_offset: int, page_size: int, name_looked: str = "") -> list[dict[str, dict]]:
        """
        Returns a list of tuples based on an offset and page size.
        ### Receives:
        - Offset
        - Name looked
        ### Returns:
        - List with dictionaries of 
        """
        try: # Probability of polimorphism with raw material! # no problem with fstrings cause it's parametized instantly by SQLAlchemy
            results: list[Product] = self.session.query(
                            Product.product_name,
                            Product.category,
                            Product.price,
                            Product.recipes
                            )\
                        .filter(Product.product_name.ilike(f"%{name_looked}%"))\
                        .filter(Product.r_id == r_id)\
                        .offset(actual_offset)\
                        .limit(page_size)\
                        .all()
        except SQLAlchemyError as e:
            raise_and_log("Unexpected server error during the products' records extraction", e, logger)
        if not results:
            raise_and_log(f"Couldn't find any results while looking for products that match '{name_looked}'", ValueError(), logger)
        return [prod._to_dict() for prod in results]
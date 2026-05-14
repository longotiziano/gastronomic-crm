from app.models.product import Product
from app.repositories.base_repository import Repository

from sqlalchemy.exc import SQLAlchemyError

from app.logs.loggers import start_logger, raise_and_log
logger = start_logger(__name__)

class ProductsRepository(Repository):
    model = Product
    name = 'product_name'
    id = 'product_id'

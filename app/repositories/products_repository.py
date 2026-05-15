from app.models.product import Product
from app.repositories.base_repository import Repository

class ProductsRepository(Repository):
    def __init__(self, session):
        super().__init__(session, Product, "product_name", "product_id")

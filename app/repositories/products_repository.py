from app.models.product import Product
from app.repositories.base_repository import Repository

class ProductsRepository(Repository[Product]):
    def __init__(self, session):
        super().__init__(session, Product, "product_name", "product_id")

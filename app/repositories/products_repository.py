from app.models.auto_models import Products, RawMaterial, Recipes
from app.repositories.base_repository import Repository

class ProductsRepository(Repository):
    model = Products
    name = 'product_name'
    id = 'product_id'

    def get_products(self):
        """
        
        """
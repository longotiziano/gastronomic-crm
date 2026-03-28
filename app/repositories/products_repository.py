from app.models.auto_models import Products, RawMaterial, Recipes
from app.repositories.base_repository import Repository
from sqlalchemy.orm import Session

class ProductsRepository(Repository):
    model = Products
    name = 'product_name'
    id = 'product_id'

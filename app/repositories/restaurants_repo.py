from app.models.restaurant import Restaurant
from app.repositories.base_repository import Repository

class RestaurantRepository(Repository):
    def __init__(self, session):
        super().__init__(session, Restaurant, "restaurant", "r_id")
from app.models.restaurant import Restaurant
from app.repositories.base_repository import Repository

from sqlalchemy.exc import SQLAlchemyError
from typing import Optional

from app.logs.loggers import start_logger, raise_and_log
logger = start_logger(__name__)

class RestaurantRepository(Repository):
    def _get_restaurants(self, looked_name: str = "", r_id: Optional[int] = None) -> list[Restaurant]:
        '''
        ### Receives:
        - A restaurant name (optional)
        - A restaurant ID (optional)
        ### Returns:
        - A list with the restaurant objects that matched the received criteria
        '''
        try:
            restaurants_list = \
                self.session.query(Restaurant)\
                .filter(Restaurant.r_id != -9999)
            
            if looked_name:
                restaurants_list = restaurants_list.filter(Restaurant.restaurant.ilike(f"%{looked_name}%"))
            
            if r_id is not None:
                restaurants_list = restaurants_list.filter(Restaurant.r_id == r_id)
            
            restaurants_list = restaurants_list.all()
        except SQLAlchemyError as e:
            raise_and_log("Unexpected error while finding the restaurants' records", e, logger)

        if not restaurants_list:
            raise_and_log("Couldn't find any restaurants' records", ValueError(), logger)

        logger.debug("Finded restaurants' list -> Records' amount: %s", len(restaurants_list))
        return restaurants_list
from app.models.restaurant import Restaurant
from app.repositories.base_repository import Repository

from sqlalchemy.exc import SQLAlchemyError

from app.logs.loggers import start_logger, raise_and_log
logger = start_logger(__name__)

class RestaurantRepository(Repository):
    def _get_restaurants(self, looked_name: str = "") -> list[int]:
        '''
        ### Receives:
        - A restaurant name (optional)
        ### Returns:
        - A list with the IDs that matched the received name
        '''
        try:
            restaurants_list = \
                [r[0] for r in self.session.query(Restaurant.r_id)\
                .filter(Restaurant.r_id != -9999)\
                .filter(Restaurant.restaurant.ilike(f"%{looked_name}%")).all()]
        except SQLAlchemyError as e:
            raise_and_log("Unexpected error while finding the restaurants' records", e, logger)

        if not restaurants_list:
            raise_and_log("Couldn't find any restaurants' records", ValueError(), logger)

        logger.debug("Finded restaurants' list -> Records' amount: %s", len(restaurants_list))
        return restaurants_list
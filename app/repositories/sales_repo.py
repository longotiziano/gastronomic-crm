from app.models.sale import Sale
from app.repositories.base_repository import Repository

from sqlalchemy.exc import SQLAlchemyError

from app.logs.loggers import start_logger, raise_and_log
logger = start_logger(__name__)

class SaleRepository(Repository):
    def get_sales(self, actual_offset: int):
        """
        Based on an offset
        ### Receives:
        - Offset 
        ### Returns:
        - 
        """
        try:
            self.session.query(Sale)
        except SQLAlchemyError as e:
            raise_and_log("Unexpected server error during the sales' records extraction", e, logger)
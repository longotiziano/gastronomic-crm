from typing import Any

from logs.loggers import start_logger
logger = start_logger(__name__)

class APIException(Exception):
    def __init__(
        self, 
        msg: str, 
        error_type: str,
        code: int = 400,
    ):
        super().__init__(msg)
        self.msg = msg
        self.error_type = error_type
        self.code = code
        
        self._log_error()

    def _log_error(self):
        logger.error("ERROR: %s | Message: %s | Code: %s", self.error_type, self.msg, self.r_id, self.code)

class InternalServerException(APIException):
    def __init__(self):
        super().__init__("Unexpected internal error occur. Try again later", "INTERNAL_SERVER_ERROR", 500)

class ResourceNotFoundException(APIException):
    def __init__(self, resource: str):
        super().__init__(f"Couldn't find the resource {resource}", "RESOURCE_NOT_FOUND", 400)

class RecordMismatchException(APIException):
    def __init__(self, expected: Any, obtained: Any, ):
        super().__init__("", code=409)

class InventoryShortageException(RecordMismatchException):
    def __init__(self, product_name):
        super().__init__(f"No hay stock suficiente para el producto: {product_name}.") 
        

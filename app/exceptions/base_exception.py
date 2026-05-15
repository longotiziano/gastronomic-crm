from typing import Any

from logs.loggers import start_logger
logger = start_logger(__name__)

class APIException(Exception):
    def __init__(
        self, 
        msg: str, 
        error_type: str,
        code: int = 400,
        data = dict
    ):
        super().__init__(msg)
        self.msg = msg
        self.error_type = error_type
        self.code = code
        self.data = data

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
    def __init__(self, expected: Any, obtained: Any, data: dict = {}):
        msg = f"Record mismatch occur. Expected: {expected}, obtained: {obtained}."
        super().__init__(msg, "RECORD_MISMATCH_ERROR", 409, data)

class InventoryShortageException(RecordMismatchException):
    def __init__(self, rm_dict: dict[str, float] = {}):
        """Receives a dict with the affected raw material and the missing amount"""
        msg = "Not enough stock to upload the sale. Missing raw material."
        super().__init__(msg, "INVENTORY_SHORTAGE_ERROR", data=rm_dict) 
        

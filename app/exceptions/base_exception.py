from typing import Any

from app.logs.loggers import start_logger
logger = start_logger(__name__)

class APIException(Exception):
    def __init__(
        self, 
        msg: str, 
        error_type: str,
        code: int = 400,
        detail: str = "",
        data: dict = {}
    ):
        super().__init__(msg)
        self.msg = msg
        self.error_type = error_type
        self.code = code
        self.detail = detail
        self.data = data

        self._log_error()

    def _log_error(self):
        logger.error("ERROR: %s | Message: %s | Code: %s | Detail: %s", self.error_type, self.msg, self.code, self.detail)

class ResourceNotFoundException(APIException):
    def __init__(self, resource_type: str, resource: str):
        super().__init__(f"Couldn't find the {resource_type} {resource}", "RESOURCE_NOT_FOUND", 404)

class MissingParametersException(APIException):
    def __init__(self, parameters: list[str]):
        super().__init__(f"Missing required parameters: {', '.join(parameters)}", "MISSING_PARAMETERS", 400)

class RecordMismatchException(APIException):
    def __init__(self, expected: Any, obtained: Any, data: dict = {}):
        msg = f"Record mismatch occur. Expected: {expected}, obtained: {obtained}."
        super().__init__(msg, "RECORD_MISMATCH_ERROR", 409, "", data)
        

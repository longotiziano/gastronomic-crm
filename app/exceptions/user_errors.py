from app.exceptions.base_exception import APIException

class DuplicateRecordException(APIException):
    def __init__(self, record_type: str, record: str):
        super().__init__(f"{record_type} '{record}' already exists", "DUPLICATE_RECORD_ERROR", 409)
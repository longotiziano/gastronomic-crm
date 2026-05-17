from app.exceptions.base_exception import APIException

class InventoryShortageException(APIException):
    def __init__(self, rm_dict: dict[str, float] = {}):
        """Receives a dict with the affected raw material and the missing amount"""
        msg = "Not enough stock to upload the sale. Missing raw material."
        super().__init__(msg, "INVENTORY_SHORTAGE_ERROR", 409, "", rm_dict) 
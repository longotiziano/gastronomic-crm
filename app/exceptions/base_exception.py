class APIException(Exception):
    def __init__(
        self, 
        msg: str, 
        error_type: str,
        r_id: int = -9999,
        code: int = 400
    ):
        super().__init__(msg)
        self.msg = msg
        self.error_type = error_type
        self.r_id = r_id
        self.code = code

class ResourceNotFoundException(APIException):
    def __init__(self, resource_name, resource_id):
        message = f"El recurso '{resource_name}' con ID {resource_id} no existe."
        super().__init__(message, status_code=404)

class RecordMismatchException(APIException):
    def __init__(self, detail_message):
        # Usamos 409 Conflict o 400 Bad Request según prefieras
        super().__init__(detail_message, status_code=409)

class InventoryShortageException(RecordMismatchException):
    def __init__(self, product_name):
        super().__init__(f"No hay stock suficiente para el producto: {product_name}.") 
        

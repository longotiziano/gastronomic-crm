from app.exceptions.base_exception import APIException

class InternalServerException(APIException):
    def __init__(self, detail: str = ""):
        super().__init__("Unexpected internal error occur. Try again later", "INTERNAL_SERVER_ERROR", 500, detail)

class CloudinaryException(APIException):
    def __init__(self, detail: str = ""):
        super().__init__("Error uploading image to Cloudinary", "CLOUDINARY_ERROR", 500, detail)
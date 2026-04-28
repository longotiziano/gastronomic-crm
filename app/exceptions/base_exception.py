class BaseException():
    def __init__(self, msg: str, error_type: str, code: int):
        self.msg = msg
        self.error_type = error_type
        self.code = code
        
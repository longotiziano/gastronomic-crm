from app.exceptions import APIException
from flask import jsonify, Blueprint

public_bp_errors = Blueprint("public_errors", __name__, url_prefix="/public/errors")

@public_bp_errors.errorhandler(APIException)
def handle_errors(error):
    return jsonify({
        "error": error.error_type,
        "message": error.msg
    }), error.code
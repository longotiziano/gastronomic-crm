from app.models import *

def create_app():
    # Blueprints 
    from app.routes.sales import sales_bp
    from app.routes.restaurants import resto_bp

    # Logger
    from app.logs.config import setup_logging
    setup_logging()

    # Database
    from app.sql.database import Base, engine
    Base.metadata.create_all(engine)

    # Cloudinary
    import config.cloudinary

    # Flask
    from flask import Flask, jsonify
    app = Flask(__name__)

    from app.exceptions.base_exception import APIException
    @app.errorhandler(APIException)
    def handle_errors(error: APIException):
        return jsonify({
            "error": error.error_type,
            "message": error.msg,
            "data": error.data
        }), error.code

    # CORS
    from flask_cors import CORS
    CORS(app)

    # Blueprints
    app.register_blueprint(sales_bp)
    app.register_blueprint(resto_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
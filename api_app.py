from app.routes.sales import sales_bp
from app.models import * # for registration

# Logger
from app.logs.config import setup_logging
setup_logging()

# Database
from app.sql.database import Base, engine
Base.metadata.create_all(engine)

# Flask
from flask import Flask
app = Flask(__name__)

# CORS
from flask_cors import CORS
CORS(app)

app.register_blueprint(sales_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
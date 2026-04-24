from webapp.routes.sales import sales_bp

from flask_cors import CORS
from flask import Flask

app = Flask(__name__)
CORS(app)

app.register_blueprint(sales_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
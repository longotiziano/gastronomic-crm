from flask import Flask
from webapp.routes.sales import inventory_bp

app = Flask(__name__)
app.register_blueprint(inventory_bp)
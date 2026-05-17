from app.repositories.products_repository import ProductsRepository
from app.sql.database import Sess
from app.utils.helpers import success_response, calculate_pagination

from flask import Blueprint, jsonify, request
from werkzeug.datastructures import FileStorage
from typing import Optional

from app.logs.loggers import start_logger
logger = start_logger(__name__)

sales_bp = Blueprint('sales', __name__, url_prefix='/sales')

@sales_bp.route('/upload', methods=['POST'])
def submit_sales_file():
    """
    Submits the sales to the database, and converts the sales into stock movements, changing the inventory
    ### Receives:
    - File
    ### Returns
    """                                
    file: Optional[FileStorage] = request.files.get('file')
    r_id = request.form.get('r_id', type=str)
    
    if not file or not r_id:
        return jsonify({"maaaal": False})
    
    logger.info("Succesfully created the response -> URL: %s", str(request.url))
    return jsonify({"success": True})

@sales_bp.route('/show', methods=['GET'])
def show_products():
    """
    Shows the products for a given restaurant
    """
    r_id = request.args.get("r_id", type=int)
    offset = request.args.get("offset", type=int, default=0)
    page_size = request.args.get("limit", type=int, default=13)
    looked_name = request.args.get("looked_name", type=str, default="")
    
    with Sess() as sess:
        prod_repo = ProductsRepository(sess)
        results = prod_repo._get_records(r_id=r_id, actual_offset=offset, page_size=page_size, product_name=looked_name)
        prods = [prod._to_dict() for prod in results]
        total_results = prod_repo._count_records(product_name=looked_name)
        
    prev, next, pages = calculate_pagination(offset, total_results, page_size)
    response = success_response("Products retrieved successfully.", {"products": prods}, str(request.url), 200, prev, next, pages)
    logger.info("Succesfully created the response -> URL: %s", str(request.url))
    return response
        
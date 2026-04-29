from app.repositories.products_repository import ProductsRepository
from app.repositories.restaurants_repo import RestaurantRepository
from app.sql.database import Sess
from app.utils.helpers import error_response, pagination_response, calculate_pagination

from flask import Blueprint, jsonify, request
from werkzeug.datastructures import FileStorage
from typing import Optional

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
    
    print(f"Recibido archivo: {file.filename}")
    return jsonify({"success": True})

@sales_bp.route('/show_products', methods=['GET'])
def show_products():
    """
    Shows the 
    ### Receives:
    - File
    ### Returns
    """     
    resto = request.args.get("restaurant", type=str)
    offset = request.args.get("offset", type=int, default=0)
    page_size = request.args.get("limit", type=int, default=10)
    looked_name = request.args.get("looked_name", type=str, default="")
    if not resto:
        return error_response("Couldn't find any selected restaurant. Please, choose a restaurant to continue.", "MISSING_PARAMETERS", 400)
    
    with Sess() as sess:
        res_repo = RestaurantRepository(sess)
        try:
            r_id = res_repo._get_restaurants(resto)[0]
        except Exception as e:
            return error_response(str(e), "INTERNAL_SERVER_ERROR", 500)
        
        prod_repo = ProductsRepository(sess)
        try: 
            results = prod_repo.get_products(r_id, offset, page_size, looked_name)
            total_results = prod_repo._count_records(looked_name)
        except Exception as e:
            return error_response(str(e), "INTERNAL_SERVER_ERROR", 500)
        
    prev, next, pages = calculate_pagination(offset, total_results, page_size)
    return pagination_response({"products": results}, prev, next, pages)
        
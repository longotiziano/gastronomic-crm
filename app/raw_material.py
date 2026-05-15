from app.repositories.products_repository import ProductsRepository
from app.repositories.restaurants_repo import RestaurantRepository
from app.sql.database import Sess
from app.utils.helpers import error_response, success_response, calculate_pagination

from flask import Blueprint, jsonify, request
from werkzeug.datastructures import FileStorage
from typing import Optional

from app.logs.loggers import start_logger
logger = start_logger(__name__)

public_rm_bp = Blueprint('public_raw_material_bp', __name__, url_prefix='/public/sales')

@sales_bp.route('/show', methods=['GET'])
def show_rms():
    """
    Shows the products for a given restaurant
    ### Receives:
    - File
    ### Returns
    """
    resto = request.args.get("r_id", type=str)
    if not resto:
        return error_response("Couldn't find any selected restaurant. Please, choose a restaurant to continue.", "MISSING_PARAMETERS", 400)
    
    with Sess() as sess:
        res_repo = RestaurantRepository(sess)
        try:
            resto = res_repo._get_restaurants(resto)[0]
            r_id = resto.r_id
        except Exception as e:
            # if e.code == 500: ...
            return error_response(str(e), "INTERNAL_SERVER_ERROR", 500)
        
        rm_repo = RawMaterialRepository(sess)
        try: 
            results = prod_repo.get_products(r_id, offset, page_size, looked_name)
            total_results = prod_repo._count_records(looked_name)
        except Exception as e:
            return error_response(str(e), "INTERNAL_SERVER_ERROR", 500)
        
    prev, next, pages = calculate_pagination(offset, total_results, page_size)
    response = success_response("Products retrieved successfully.", {"products": results}, str(request.url), 200, prev, next, pages)
    logger.info("Succesfully created the response -> URL: %s", str(request.url))
    return response
        

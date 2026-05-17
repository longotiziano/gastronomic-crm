from app.repositories.raw_material_repository import RawMaterialRepository
from app.repositories.restaurants_repo import RestaurantRepository
from app.sql.database import Sess
from app.utils.helpers import error_response, success_response, calculate_pagination

from flask import Blueprint, request

from app.logs.loggers import start_logger
logger = start_logger(__name__)

from app.logs.config import BASE_DIR
import json
CONFIG_FILE = BASE_DIR / "config" / "config.json"
with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

public_rm_bp = Blueprint('public_raw_material_bp', __name__, url_prefix='/public/raw_materials')

@public_rm_bp.route('/show', methods=['GET'])
def show_rms():
    """
    Shows the raw materials for a given restaurant
    ### Receives:
    - File
    ### Returns
    """
    r_id = request.args.get("r_id", type=int, default=config["default_values"]["default_restaurant"])
    logger.debug("Obtained the restaurant id -> r_id: %s | Default: %s", r_id, config["default_values"]["default_restaurant"])

    with Sess() as sess:
        rm_repo = RawMaterialRepository(sess)
        results = rm_repo._get_records(r_id=r_id, actual_offset=actual_offset, page_size=page_size, looked_name=looked_name)
        rms = [rm._to_dict() for rm in results]
        total_results = rm_repo._count_records(looked_name)
        
    prev, next, pages = calculate_pagination(offset, total_results, page_size)
    response = success_response("Raw materials retrieved successfully.", {"raw_materials": results}, str(request.url), 200, prev, next, pages)
    logger.info("Succesfully created the response -> URL: %s", str(request.url))
    return response
        

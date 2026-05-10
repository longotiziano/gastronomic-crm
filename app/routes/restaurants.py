from app.models.restaurant import Restaurant
from app.repositories.restaurants_repo import RestaurantRepository
from app.sql.database import Sess
from app.utils.helpers import error_response, calculate_pagination, success_response

from flask import Blueprint, jsonify, request

from app.logs.loggers import start_logger
logger = start_logger(__name__)

resto_bp = Blueprint('restaurants', __name__, url_prefix='/restaurants')

@resto_bp.route('/creation', methods=['POST'])
def create_restaurant():
    """
    Creates a restaurant
    """
    data = request.get_json(silent=True)
    if not data:
        return error_response(f"Didn't receive any required parameters to create the restaurant", "MISSING_PARAMETERS", 400)
    
    with Sess() as sess:
        res_repo = RestaurantRepository(sess)
        try:
            restos = res_repo._get_restaurants(data["restaurant"])[0]
        except Exception as e:
            return error_response(str(e), "INTERNAL_SERVER_ERROR", 500)
        
        if not restos:
            try:
                new_resto = Restaurant(name=data["restaurant"], image_url=data["image_url"])
                sess.add(new_resto)
                sess.commit()
                sess.refresh(new_resto)
            except Exception as e:
                return error_response(str(e), "INTERNAL_SERVER_ERROR", 500)
        else:
            return error_response(f"Couldn't create the restaurant because there is already a restaurant with the same name", "RESTAURANT_ALREADY_EXISTS", 400)
    
    logger.info("Created the restaurant -> ID: %s | Name: %s", new_resto.r_id, new_resto.restaurant)
    return success_response("Restaurant created successfully", {"restaurant": new_resto._to_dict()}, str(request.url), 201)

@resto_bp.route('/show', methods=['GET'])
def show_restaurants():
    """
    Shows the restaurants
    """
    with Sess() as sess:
        res_repo = RestaurantRepository(sess)
        try:
            restos = res_repo._get_restaurants()
        except Exception as e:
            return error_response(str(e), "INTERNAL_SERVER_ERROR", 500)

    logger.info("Succesfully created the response -> URL: %s", str(request.url))
    return success_response("Restaurants found successfully", {"restaurants": [resto._to_dict() for resto in restos]}, str(request.url), 200)
        
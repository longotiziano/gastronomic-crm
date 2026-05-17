from app.exceptions.base_exception import MissingParametersException
from app.models.restaurant import Restaurant
from app.repositories.restaurants_repo import RestaurantRepository
from app.sql.database import Sess
from app.utils.helpers import success_response

from flask import Blueprint, request

from app.logs.loggers import start_logger
logger = start_logger(__name__)

resto_bp = Blueprint('public_restaurants', __name__, url_prefix='/public/restaurants')

@resto_bp.route('/creation', methods=['POST'])
def create_restaurant():
    restaurant = request.form.get('restaurant')
    logo = request.files.get('image_url', default=None)
    logger.debug("Received data for restaurant creation -> Data: %s | URL: %s", restaurant, str(request.url))
    if not restaurant:
        raise MissingParametersException(["restaurant"])
    
    with Sess() as sess:
        res_repo = RestaurantRepository(sess)
        new_resto = res_repo.create_record(restaurant=restaurant, image_url=logo)

    logger.info("Created the restaurant -> ID: %s | Name: %s", new_resto.r_id, new_resto.restaurant)
    return success_response("Restaurant created successfully", {"restaurant": new_resto._to_dict()}, str(request.url), 201)

@resto_bp.route('/show', methods=['GET'])
def show_restaurants():
    with Sess() as sess:
        res_repo = RestaurantRepository(sess)
        restos: list[Restaurant] = res_repo._get_records()
    logger.info("Succesfully created the response -> URL: %s", str(request.url))
    return success_response("Restaurants found successfully", {"restaurants": [resto._to_dict() for resto in restos]}, str(request.url), 200)
        
from flask import Blueprint, jsonify, request

inventory_bp = Blueprint('sales', __name__)

@inventory_bp.route('/sales', methods=['GET'])
def process_sales_to_rm():
    """
    ### Receives:
    - File
    ### Returns
    """
    r_id = request.args.get("restaurant", type=int)
    return jsonify({"success": True})
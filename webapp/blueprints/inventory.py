from flask import Blueprint, jsonify

inventory = Blueprint('ventas', __name__)

@inventory.route('/inventario', methods=['GET'])
def process_sales_to_rm():
    """
    ### Receives:
    - File
    ### Returns
    """
    return jsonify({"success": True})
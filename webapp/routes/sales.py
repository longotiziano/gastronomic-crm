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
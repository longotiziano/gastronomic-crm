from flask import Response, jsonify

def calculate_pagination(actual_offset: int, total_records: int, page_size: int) -> tuple[int, int, int]:
    """
    Calculates offset for pagination
    ### Receives:
    - Actual offset
    - Total records
    ### Returns:
    - Previous page offset
    - Next page offset
    - Total pages
    """
    num_pages = -(-total_records // page_size) # trick
    prev_page = 0 if actual_offset < page_size else actual_offset - page_size
    next_page = total_records if actual_offset + page_size >= total_records else actual_offset + page_size
    return prev_page, next_page, num_pages

def error_response(msg: str, error_type: str, code: int) -> tuple[Response, int]:
    return jsonify({
        'msg': msg,
        'error_type': error_type
    }), code

def success_response(
        msg: str, 
        data: dict, 
        url: str, 
        code: int,
        prev_offset: int = 0, 
        next_offset: int = 0, 
        total_pages: int = 0
    ) -> tuple[Response, int]:
    return jsonify({
        'msg': msg,
        'data': data,
        "pagination": {
            "prev_offset": prev_offset,
            "next_offset": next_offset,
            "total_pages": total_pages
            },
        'meta': {
            'url': url
        }
    }), code

def upload_image(file) -> str:
    """
    Uploads the image to the server and returns the URL
    ### Receives:
    - File
    ### Returns:
    - URL of the uploaded image
    """
    # Aquí iría la lógica para subir la imagen a un servicio de almacenamiento (como AWS S3, Google Cloud Storage, etc.)
    # y luego devolver la URL de la imagen subida.
    # Por simplicidad, vamos a simular esto devolviendo una URL ficticia.
    return f"https://example.com/images/{file.filename}"


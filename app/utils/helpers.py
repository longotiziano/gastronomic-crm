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

def pagination_response(data: dict, prev_offset: int, next_offset: int, total_pages: int) -> tuple[Response, int]:
    return jsonify({
        "data": data,
        "pagination": {
            "prev_offset": prev_offset,
            "next_offset": next_offset,
            "total_pages": total_pages
            }
    }), 200

def error_response(msg: str, error_type: str, code: int) -> tuple[Response, int]:
    return jsonify({
        'msg': msg,
        'error_type': error_type
    }), code
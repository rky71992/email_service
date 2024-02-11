from flask import jsonify, Response
from db import session
from models import Services

def my_abort(error: dict, custom_message: str = '') -> Response:
    """Abort and return an error code json response
    Args:
        error-- defined in error.py
    Returns:
        The response in JSON
        {
            "error": {
                "title": "string",
                "message": "string"
            }
        }
    """
    msg = custom_message if custom_message else str(error.get('message',''))
    res = jsonify({"error": {"title": str(error.get('title','')), "message": msg}})
    res.status_code = error['code']
    return res

def get_service_by_name(service_name):
    service = session.query(Services).filter_by(service_name=service_name).one_or_none()
    return service
import logging
from flask import Blueprint, request, jsonify
from definations import NewUser
import utils
import jwt
from db import session
from errors import *
from models import Users
import bcrypt
from config import UTF_8, JWT_SECRET_KEY
from functools import wraps
from flask import current_app, abort
#import models

logger = logging.getLogger("auth.{}".format(__name__))
auth_bp = Blueprint('auth_blueprint', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if ('username' not in data) or ('password' not in data):
        return utils.my_abort(MISSING_REQUIRED_PARAMETER)
    
    user = session.query(Users).filter_by(username=data['username']).one_or_none()
    if not user:
        return utils.my_abort(INVALID_AUTHENTICATION)
    
    if not bcrypt.checkpw(data['password'].encode(UTF_8), user.password.encode(UTF_8)):
        return utils.my_abort(INVALID_AUTHENTICATION)
    
    token = jwt.encode({"user_id": user.id}, JWT_SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token.decode(UTF_8)})



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(data["user_id"], *args, **kwargs)

    return decorated


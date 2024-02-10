from flask import Blueprint, request, Response, jsonify
import logging
from auth.authentication import token_required
from utils import my_abort
from errors import *
from definations import NewServiceRegister
from db import session
from models import UserServices

logger = logging.getLogger("mail.{}".format(__name__))
mail_bp = Blueprint('mail_blueprint', __name__)


@mail_bp.route('/send-mail',methods=['POST'])
@token_required
def send_mail_service(user_id: int):
    data: dict = request.get_json()
    if not data or not data.get('services'):
        return my_abort(MISSING_REQUIRED_PARAMETER)
    
    services: list[dict] = data['services']
    validated_services: list[NewServiceRegister] = []
    for service in services:
        try:
            service['user_id'] = user_id
            new_service: NewServiceRegister = NewServiceRegister(**service)
            validated_services.append(new_service)
        except Exception as ex:
            logger.exception(f'Not able to register new service: {ex}')
            my_abort(INVALID_PARAMETER)

    for service in validated_services:
        session.add(UserServices(**service.model_dump()))
    session.commit()
    return jsonify({'success':True})
    

@mail_bp.route('/mail-status/<id>',methods=['GET'])
@token_required
def mail_status(user_id: int, mail_id: int | None):
    pass

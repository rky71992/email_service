from flask import Blueprint, request, Response, jsonify
import logging
from auth.authentication import token_required
from utils import my_abort
from errors import *
from definations import NewServiceRegister
from db import session

logger = logging.getLogger("service.{}".format(__name__))
service_bp = Blueprint('mail_blueprint', __name__)


@service_bp.root_path('/add-service',methods=['POST'])
@token_required
def add_mail_service(user_id: int):
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
        session.add(service.model_dump())
    session.commit()
    return jsonify({'success':True})
    

@service_bp.root_path('/registered-service',methods=['GET'])
@token_required
def get_user_mail_service(user_id):
    pass

@service_bp.root_path('/update-service',methods=['POST'])
@token_required
def update_user_mail_service(user_id):
    pass


@service_bp.root_path('/delete-service',methods=['GET'])
@token_required
def get_user_mail_service(user_id):
    pass

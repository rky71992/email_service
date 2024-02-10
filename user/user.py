import logging
from flask import Blueprint, request, jsonify
from definations import NewUser
import utils
from db import session
from errors import MISSING_REQUIRED_PARAMETER, INVALID_PARAMETER
from models import Users, Services, UserServices
from auth.authentication import token_required

logger = logging.getLogger("user.{}".format(__name__))
user_bp = Blueprint('user_blueprint', __name__)



@user_bp.route('/create-user', methods=['POST'])
def create_new_user():
    data = request.get_json()
    try:
        new_user = NewUser(**data)
    except Exception as ex:
        logger.exception(f'Error creating new user: {ex}')
        return utils.my_abort(MISSING_REQUIRED_PARAMETER)
    
    existing_user = session.query(Users).filter_by(username=new_user.username).one_or_none()
    if existing_user:
        return utils.my_abort(INVALID_PARAMETER,custom_message='username already exists')
    
    user_data = Users(**new_user.model_dump())
    session.add(user_data)
    session.commit()
    logger.info(f'New user created: {new_user.username}')

    return jsonify({'success':True,'user':new_user.username,'message':'User created successfull'})
    

@user_bp.route('/user', methods=['GET'])
@token_required
def get_user_details(user_id):
    user = session.query(Users).filter_by(id=user_id).one()
    data = user.serialize()
    services: dict = {}
    available_services: list = []
    user_registered_services: list = []
    master_services = session.query(Services).all()
    for service in master_services:
        available_services.append(service.service_name)
    services['available_services'] = available_services

    user_db_services = session.query(UserServices,Services).join(Services).filter(UserServices.user_id == user_id).all()
    for user_service, service in user_db_services:
        user_registered_services.append({'service_name':service.service_name, 'sender_email':user_service.sender_email})
    services['registered_services'] = user_registered_services
    
    data['services'] = services
    return jsonify(data)



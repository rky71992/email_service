import logging
from flask import Blueprint, request, jsonify
from definations import NewUser, NewServiceRegister
import utils
from db import session
from errors import MISSING_REQUIRED_PARAMETER, INVALID_PARAMETER
from models import Users, Services, UserServices
from auth.authentication import token_required
from utils import my_abort

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


@user_bp.route('/user/add-service',methods=['POST'])
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
        session.add(UserServices(**service.model_dump()))
    session.commit()
    return jsonify({'success':True})
    

@user_bp.route('/user/update-service',methods=['POST'])
@token_required
def update_user_mail_service(user_id):
    pass


@user_bp.route('/user/delete-service',methods=['DELETE'])
@token_required
def delete_user_mail_service(user_id):
    data: dict = request.get_json()
    if 'services' not in data and isinstance(data.get('services'),list):
        return my_abort(MISSING_REQUIRED_PARAMETER)
    
    service_delete_response : list = []
    for service in data['services']:
        service_resp = {'service_name':service}
        service_resp['error'] = ''
        master_service = session.query(Services).filter_by(service_name=service).one_or_none()
        if not master_service:
            service_resp['status'] = False
            service_resp['error'] = "There is no service supported by this name"
            service_delete_response.append(service_resp)
            continue
        user_registered_service = session.query(UserServices).filter_by(user_id=user_id,service_id=master_service.id).one_or_none()
        if not user_registered_service:
            service_resp['status'] = False
            service_resp['error'] = "User have not registered this service"
            service_delete_response.append(service_resp)
            continue

        session.delete(user_registered_service)
        session.commit()
        service_resp['status'] = True
        service_delete_response.append(service_resp)
    
    return jsonify({"services":service_delete_response})


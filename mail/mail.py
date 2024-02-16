from flask import Blueprint, request, Response, jsonify
import logging
from auth.authentication import token_required
from utils import my_abort, get_rabbitmq_connection
from errors import *
import uuid
from definations import NewServiceRegister, NewMailRequest, MailStatus
from db import session
from models import UserServices, UserMail
from config import MAIL_QUEUE

logger = logging.getLogger("mail.{}".format(__name__))
mail_bp = Blueprint('mail_blueprint', __name__)


@mail_bp.route('/send-mail',methods=['POST'])
@token_required
def send_mail_service(user_id: int):
    data: dict = request.get_json()
    try:
        new_mail_data: NewMailRequest = NewMailRequest(**data)
    except Exception as ex:
        logger.exception(f'Not able to new mail request: {ex}')
        return my_abort(MISSING_REQUIRED_PARAMETER)
    
    mail_db_data: dict = new_mail_data.model_dump()
    unique_id = str(uuid.uuid4())
    mail_db_data['mail_unique_id'] = unique_id
    mail_db_data['user_id'] = user_id
    mail_db_data['mail_status'] = MailStatus.QUEUED
    session.add(UserMail(**mail_db_data))
    session.commit()

    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key=MAIL_QUEUE, body=f'{unique_id}')

    return jsonify({'status':MailStatus.QUEUED, 'id':unique_id})

    

@mail_bp.route('/mail-status',methods=['GET'])
@token_required
def mail_status(user_id: int):
    mail_id_requested = request.args.get('mail_id')

    query = session.query(UserMail).filter_by(user_id=user_id)
    if mail_id_requested:
        query = query.filter_by(mail_unique_id=mail_id_requested)
    result = query.all()

    mail_status_list: list = []
    for mails in result:
        mail_status_list.append(mails.serialize())
        
    return jsonify({'mail_status':mail_status_list})
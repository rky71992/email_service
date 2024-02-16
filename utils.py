from flask import jsonify, Response
from db import session
from models import Services
import pika
from config import MAIL_QUEUE

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

def setup_rabbitmq() -> None:
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    
    channel = connection.channel()
    channel.queue_declare(queue=MAIL_QUEUE)
    #connection.close()

class RabbitMQSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RabbitMQSingleton, cls).__new__(cls)
            cls._instance.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        return cls._instance

    def get_connection(self):# -> Any:
        return self.connection

def get_rabbitmq_connection():# -> Any:
    redis_instance = RabbitMQSingleton()
    return redis_instance.get_connection()
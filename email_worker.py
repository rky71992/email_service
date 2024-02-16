import pika, sys, os
from config import MAIL_QUEUE
import logging
from db import session
from mailservice import MailService
from models import UserMail,Services,UserServices
from definations import MailStatus

logger = logging.getLogger("user.{}".format(__name__))

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()


    def process_message(ch, method, properties, body):
        logger(f"Unique ID: {body} recieved for processing--{body}")
        db_msg: UserMail = session.query(UserMail).filter_by(mail_unique_id=body).one_or_none()
        if not db_msg:
            logger.error(f'Unique ID: {body} Something is wrong: {body} is not present in DB')
            return
        
        if db_msg.mail_status in [MailStatus.FAILED,MailStatus.SUCCESS]:
            logger.info(f'Unique ID: {body} is already processed')
            return
        
        db_user_services = session.query(UserServices).filter_by(user_id=db_msg.user_id).all()
        if not db_user_services:
            logger.info(f'Unique ID: {body} cannot be processed, no mail services registered for the user')
            db_msg.mail_status = MailStatus.FAILED
            session.add(db_msg)
            session.commit()
            return
        
        
        





    channel.basic_consume(queue=MAIL_QUEUE, on_message_callback=process_message, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
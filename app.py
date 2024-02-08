from flask import Flask

from auth.authentication import auth_bp
from mail.services import service_bp
from user.user import user_bp
from config import API_VERSION

app = Flask(__name__)

app.register_blueprint(user_bp,url_prefix=f'/{API_VERSION}')
app.register_blueprint(service_bp,url_prefix=f'/{API_VERSION}')
app.register_blueprint(auth_bp,url_prefix=f'/{API_VERSION}')


if __name__ == '__main__':
   app.run()
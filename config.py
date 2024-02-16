import os
from dotenv import load_dotenv

load_dotenv()

API_VERSION = "v1"
DATABASE_URL = os.getenv('DATABASE_URL')
UTF_8 = 'utf-8'
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or 'ThisIsJWTSecretKey'
MAIL_QUEUE = 'mail-queue'
import pydantic
import bcrypt
from email_validator import validate_email
from typing import  Optional
from utils import get_service_by_name

from config import UTF_8

class MailStatus:
    QUEUED = 'queued'
    FAILED = 'failed'
    SUCCESS = 'success'

class NewUser(pydantic.BaseModel):
    name: str
    username: str
    password: str

    @pydantic.field_validator("name")
    @classmethod
    def name_validator(cls, value) -> str:
        if not value.strip():
            raise ValueError
        return value.strip()

    @pydantic.field_validator("username")
    @classmethod
    def username_validator(cls, value) -> str:
        if not value.strip():
            raise ValueError
        return value.strip()
    
    @pydantic.field_validator("password")
    @classmethod
    def passwod_validator_hasher(cls, value) -> str:
        if not value.strip():
            raise ValueError
        text_password = value.strip()
        hash_pwd = bcrypt.hashpw(text_password.encode(UTF_8),bcrypt.gensalt())
        return hash_pwd.decode(UTF_8)


class   NewServiceRegister(pydantic.BaseModel):
    user_id: int
    service_name: str
    key: str
    sender_email: str

    @pydantic.field_validator("key")
    @classmethod
    def username_validator(cls, value) -> str:
        if not value.strip():
            raise ValueError
        return value.strip()

    @pydantic.field_validator("sender_email")
    @classmethod
    def recievers_validator(cls, value) -> str:
        email_info = validate_email(value, check_deliverability=False)
        return email_info.normalized
    
    @pydantic.field_validator("service_name")
    @classmethod
    def service_name_validator(cls, value) -> str:
        if not value.strip():
            raise ValueError
        return value.strip()

    
class NewMailRequest(pydantic.BaseModel):
    text: str
    subject: str
    recievers: list


import pydantic
import bcrypt

from config import UTF_8


class NewUser(pydantic.BaseModel):
    name: str
    username: str
    password: str

    @pydantic.validator("name")
    @classmethod
    def name_validator(cls, value) -> str:
        if not value.strip():
            raise ValueError
        return value.strip()

    @pydantic.validator("username")
    @classmethod
    def username_validator(cls, value) -> str:
        if not value.strip():
            raise ValueError
        return value.strip()
    
    @pydantic.validator("password")
    @classmethod
    def passwod_validator_hasher(cls, value) -> str:
        if not value.strip():
            raise ValueError
        text_password = value.strip()
        hash_pwd = bcrypt.hashpw(text_password.encode(UTF_8),bcrypt.gensalt())
        return hash_pwd.decode(UTF_8)

    
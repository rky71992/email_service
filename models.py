from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql import func

from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint, Column, \
    Boolean, Integer, String, DateTime, \
    ForeignKey, text, ARRAY, JSON

from sqlalchemy import ForeignKey

class CustomBase:
    """
    Abstract base class model.

    Abstract base class model provides self updating ``created`` and
    ``modified`` fields.
    """

    @declared_attr
    def __tablename__(cls):
        """Tablename in lower case."""
        return cls.__name__.lower()

    created = Column(DateTime, nullable=False, default=func.now(),server_default=text('NOW()::timestamp'), index=True)
    modified = Column(DateTime, nullable=False, default=func.now())


# The Base class
Base = declarative_base(cls=CustomBase)


class Users(Base):
    """
    Model for the Users.
    """

    __tablename__ = 'users'
    __table_args__ = (PrimaryKeyConstraint('id'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, comment='The name of the user')
    username = Column(String, nullable=False, comment='Username which he will use for login')
    password = Column(String, nullable=False, comment='password of the user')
    
    def serialize(self) -> dict:
        """Return dictionary of users."""
        out = {}
        out['id'] = int(self.id)
        out['name'] = str(self.name)
        out['username'] = str(self.username)
        return out


class Services(Base):
    """
    Model for the Services that are supported.
    """

    __tablename__ = 'services'
    __table_args__ = (PrimaryKeyConstraint('id'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String, nullable=False, comment='The name of the service')
    
    def serialize(self) -> dict:
        """Return dictionary of services"""
        out = {}
        out['service_name'] = str(self.service_name)
        return out


class UserServices(Base):
    """
    Model for the mail services registered by the user.
    """

    __tablename__ = 'user_services'
    __table_args__ = (PrimaryKeyConstraint('id'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), comment='User primary key')
    service_id = Column(Integer, ForeignKey('services.id'), comment='Services primary key')
    key = Column(String, nullable=False, comment='Key used for authentication in mail service')
    sender_email = Column(String, nullable=False, comment='The email of the user used for this service')
    
    def serialize(self) -> dict:
        """Return dictionary of user resgistered services"""
        out = {}
        out['sender_email'] = str(self.sender_email)
        return out
    

class UserMail(Base):
    """
    Model for the mail send by user.
    """

    __tablename__ = 'user_mail'
    __table_args__ = (PrimaryKeyConstraint('id'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    mail_unique_id = Column(String, nullable=False, comment='Unique of the mail')
    user_id = Column(Integer, ForeignKey('users.id'), comment='User primary key')
    mail_status = Column(String, nullable=False, comment='Status of the mail')
    recievers = Column(ARRAY(String), nullable=False, comment='Recievers mail id list')
    text = Column(String, nullable=False, comment='Body of the data to send')
    subject = Column(String, nullable=False, comment='Subject of mail to send')

    def serialize(self) -> dict:
        """Return dictionary of user sent mails"""
        out = {}
        out['mail_id'] = self.mail_unique_id
        out['mail_status'] = str(self.mail_status)
        out['subject'] = self.subject
        out['text'] = self.text
        out['recievers'] = self.recievers
        
        return out
    
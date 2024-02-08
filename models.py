from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql import func

from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint, Column, \
    Boolean, Integer, String, DateTime, \
    ForeignKey, text, ARRAY, JSON

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
    Model for the events that has occured.
    """

    __tablename__ = 'users'
    __table_args__ = (PrimaryKeyConstraint('id'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, comment='The name of the user')
    username = Column(String, nullable=False, comment='Username which he will use for login')
    password = Column(String, nullable=False, comment='password of the user')
    
    def serialize(self):
        """Return dictionary of event logs."""
        out = {}
        out['id'] = int(self.id)
        out['name'] = str(self.name)
        out['username'] = str(self.username)
        return out
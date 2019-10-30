"""
PostgreSQL SQLAlchemy table models.
"""
import uuid
from datetime import datetime
from typing import Tuple, Union

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TIMESTAMP, Boolean


Base = declarative_base()

USERS_TABLE = "users"
TABLES = [USERS_TABLE]


def generate_uuid() -> str:
    """
    Return uuid.
    """

    return str(uuid.uuid4())


class Text2LexTable:
    """
    General table class.
    """

    def as_dict(self):
        """
        Return item as dict.
        """

        d = {}
        columns = self.__table__.columns  # pylint: disable=E1101
        for column in columns:
            d[column.name] = getattr(self, column.name)

        return d


class User(Base, Text2LexTable):
    """
    Outbookers user model.
    """

    __tablename__ = USERS_TABLE

    id = Column(String(48), primary_key=True, default=generate_uuid)
    username = Column(String(48), unique=True, nullable=False)
    password = Column(String(96), nullable=False)
    is_admin = Column(Boolean, default=False)

    created = Column(TIMESTAMP, default=datetime.utcnow().isoformat())
    updated = Column(
        TIMESTAMP,
        onupdate=datetime.utcnow().isoformat(),
        default=datetime.utcnow().isoformat(),
    )

    def is_active(self):
        """
        Return True if user is active.
        """

        return True

    def get_id(self):
        """
        Return user id.
        """

        return self.id

    def is_authenticated(self):
        """
        No idea.
        """

        return False


ProjectModels = Tuple[User]
ProjectModel = Union[User]

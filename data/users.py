import datetime

from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import orm
from sqlalchemy.orm import Mapped, relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from data.tests import Test


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, nullable=True)
    email: Mapped[str] = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)
    tests = relationship(Test)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
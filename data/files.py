import datetime

from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from sqlalchemy.orm import Mapped
from flask_login import UserMixin


class File(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, nullable=False)
    path: Mapped[str] = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)
    answer_id: Mapped[int] = Column(Integer, ForeignKey('Answers.id'), nullable=False)


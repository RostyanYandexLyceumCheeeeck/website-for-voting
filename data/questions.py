from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from flask_login import UserMixin
from data.answers import Answer


class Question(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, nullable=False)
    description: Mapped[str] = Column(String, nullable=True)
    test_id: Mapped[int] = Column(Integer, ForeignKey('Tests.id'), nullable=False)
    answers = relationship(Answer)


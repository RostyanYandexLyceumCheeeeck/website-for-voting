import datetime

from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

from sqlalchemy.orm import Mapped, relationship
from flask_login import UserMixin
from data.files import File


class Answer(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, nullable=False)
    file_id: Mapped[int] = Column(Integer, ForeignKey('Files.id'), nullable=False)
    description: Mapped[str] = Column(String, nullable=True)
    question_id: Mapped[int] = Column(Integer, ForeignKey('Questions.id'), nullable=False)
    file = relationship(File)

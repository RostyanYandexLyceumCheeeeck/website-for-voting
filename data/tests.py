import datetime

from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase
from sqlalchemy import Column, Integer, String, DateTime, Boolean, select, ForeignKey
from sqlalchemy.orm import Mapped, relationship, selectinload
from flask_login import UserMixin

from data.answers import Answer


class Test(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Tests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, nullable=False)
    description: Mapped[str] = Column(String, nullable=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey('Users.id'), nullable=False)
    image: Mapped[str] = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)
    is_published: Mapped[bool] = Column(Boolean, default=False)
    answers = relationship(Answer, uselist=True)
    count_finished = Column(Integer, default=0)
    score = Column(Integer, default=0)

    def get_test(self, session, test_id: int) -> dict:
        """
        :param test_id: id теста
        :return: dict
        Возвращает всю информацию о тесте в виде словаря.
        """
        query = select(Test).where(Test.id == test_id).options(
            selectinload(Test.answers).joinedload(Answer.file))

        test = session.scalar(query)
        return test.to_dict()

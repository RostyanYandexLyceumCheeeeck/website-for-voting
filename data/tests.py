import datetime

from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase
from sqlalchemy import Column, Integer, String, DateTime, Boolean, select, insert, ForeignKey

from sqlalchemy.orm import Mapped, relationship, selectinload
from flask_login import UserMixin

from data.answers import Answer
from data.files import File


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

    def get_test(self, session, test_id: int):
        """
        :param test_id: id теста
        Возвращает всю информацию о тесте в виде словаря.
        """
        query = select(Test).where(Test.id == test_id).options(
            selectinload(Test.answers).joinedload(Answer.file))

        test = session.scalar(query)
        return test.to_dict()

    def insert_test(self, session, **my_test):
        """
        Записывает в БД тест во все нужные таблицы.
        :param session: сессия, подключённая к БД
        :param my_test: словарь с данными теста
        :return: None
        """
        answers = my_test.pop('answers')
        test = Test(**my_test)
        session.add(test)
        session.flush()

        for answer_data in answers:
            file_data = answer_data.pop('file')
            answer_data['test_id'] = test.id
            answer = Answer(**answer_data)
            test.answers.append(answer)
            session.add(answer)
            session.flush()

            file_data['answer_id'] = answer.id
            file = File(**file_data)
            session.add(file)
            answer.file = file
        session.commit()

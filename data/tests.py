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
    type: Mapped[str] = Column(String, nullable=False, default='Image')
    image: Mapped[str] = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)
    is_published: Mapped[bool] = Column(Boolean, default=False)
    answers = relationship(Answer)

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
        for answer_data in my_test['answers']:
            file_data = answer_data['file']
            time = datetime.datetime.strptime(file_data['created_date'], '%Y-%m-%d %H:%M:%S')
            file = File(name=file_data['name'], path=file_data['path'], created_date=time, answer_id=file_data['answer_id'])
            session.add(file)

            answer = Answer(name=answer_data['name'], description=answer_data['description'],
                            test_id=answer_data['test_id'])
            session.add(answer)

        time = datetime.datetime.strptime(my_test['created_date'], '%Y-%m-%d %H:%M:%S')
        test = Test(name=my_test['name'], description=my_test['description'], type=my_test['type'],
                    image=my_test['image'], created_date=time,
                    is_published=my_test['is_published'], answers=[answer], user_id=my_test['user_id'])
        session.add(test)
        session.commit()

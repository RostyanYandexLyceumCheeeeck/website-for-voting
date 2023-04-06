import datetime

from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase
from sqlalchemy import Column, Integer, String, DateTime, Boolean, select, insert

from sqlalchemy.orm import Mapped, relationship, selectinload
from flask_login import UserMixin

from data.questions import Question
from data.answers import Answer
from data.files import File


class Test(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'Tests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, nullable=False)
    description: Mapped[str] = Column(String, nullable=True)
    type: Mapped[str] = Column(String, nullable=False, default='Image')
    image: Mapped[str] = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)
    is_published: Mapped[bool] = Column(Boolean, default=False)
    questions = relationship(Question)

    def get_test(self, session, test_id: int):
        """
        :param test_id: id теста
        Возвращает всю информацию о тесте в виде словаря.
        """
        query = select(Test).where(Test.id == test_id).options(
            selectinload(Test.questions).joinedload(Question.answers).joinedload(Answer.file))

        test = session.scalar(query)
        return test.to_dict()

    def insert_test(self, session, **my_test):
        """
        Записывает в БД тест во все нужные таблицы.
        :param session: сессия, подключённая к БД
        :param my_test: словарь с данными теста
        :return: None
        """
        for question_data in my_test['questions']:
            for answer_data in question_data['answers']:
                file_data = answer_data['file']
                time = datetime.datetime.strptime(file_data['created_date'], '%Y-%m-%d %H:%M:%S')
                file = File(name=file_data['name'], path=file_data['path'], created_date=time)
                session.add(file)

                answer = Answer(name=answer_data['name'], description=answer_data['description'], file_id=file.id,
                                question_id=answer_data['question_id'])
                session.add(answer)

            question = Question(name=question_data['name'], description=question_data['description'],
                                    test_id=question_data['test_id'], answers=[answer])
            session.add(question)
        time = datetime.datetime.strptime(my_test['created_date'], '%Y-%m-%d %H:%M:%S')
        test = Test(name=my_test['name'], description=my_test['description'], type=my_test['type'],
                    image=my_test['image'], created_date=time,
                    is_published=my_test['is_published'], questions=[question])
        session.add(test)
        session.commit()

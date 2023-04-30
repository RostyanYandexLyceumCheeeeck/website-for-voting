from data.__all_models import *


def get_all_tests(session, user_id: int | None, private=False, rung_up=True, name='') -> list:
    filters = []
    if name:
        filters.append(Test.name.ilike(f'%{name}%'))
    if user_id:
        filters.append((Test.user_id == user_id))
    filters.append(Test.is_published != private)
    tests = session.query(Test).filter(*filters).all()
    tests.sort(key=lambda x: x.score, reverse=rung_up)
    return tests


def insert_test(session, tests: list[dict]):
    """
    Записывает в БД тест во все нужные таблицы.
    :param session: сессия, подключённая к БД
    :param tests: лист словарей с данными теста
    :return: None
    """
    for my_test in tests:
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



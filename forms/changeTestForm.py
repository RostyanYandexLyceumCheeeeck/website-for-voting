from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField


class ChangeForm(FlaskForm):
    private = SelectField('priv', choices=[('1', 'Публичный'), ('2', 'Приватный')])
    whose = SelectField('who', choices=[('1', 'Мои тесты'), ('2', 'Все тесты')])
    ranking = SelectField('rung', choices=[('1', 'Рейтинг (по возрастанию)'), ('2', 'Рейтинг (по убыванию)')])
    submit_filter = SubmitField('Применить фильтры')
    name = StringField('Название теста', default='')
    tests = list()
    is_auth = False
    is_admin = False

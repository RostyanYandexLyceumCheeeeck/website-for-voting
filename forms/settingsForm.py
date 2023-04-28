from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, MultipleFileField, TextAreaField
from wtforms.validators import DataRequired


class SettingsForm(FlaskForm):

    photo = MultipleFileField('Загрузить')
    email = EmailField('Почта')
    password_last = PasswordField("Старый пароль")
    password = PasswordField('Пароль')
    password_again = PasswordField('Повторите пароль')
    name = StringField('Логин')
    bio = TextAreaField("О себе")
    submit_save = SubmitField('Сохранить')
    submit_reset = SubmitField('Сбросить')
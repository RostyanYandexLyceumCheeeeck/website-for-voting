from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, TextAreaField, FileField
from datetime import datetime


class SettingsForm(FlaskForm):

    download_img = FileField('Загрузить')
    email = EmailField('Почта')
    password_last = PasswordField("Старый пароль")
    password = PasswordField('Пароль')
    password_again = PasswordField('Повторите пароль')
    name = StringField('Никнейм')
    bio = TextAreaField("О себе")
    submit_save = SubmitField('Сохранить')
    submit_reset = SubmitField('Сбросить')
    message = str()
    path_avatar = '/static/images/right.png'
    created_date = None

    def set_form(self, user, message=''):
        self.path_avatar = user.image
        self.email.data = user.email
        self.name.data = user.name
        self.bio.data = user.description
        self.message = message
        self.created_date = "На сайте с \n" + datetime.strftime(user.created_date, "%A\n%d %B %Y")

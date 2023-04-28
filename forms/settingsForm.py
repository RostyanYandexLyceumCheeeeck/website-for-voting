from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, MultipleFileField, TextAreaField, FileField
from wtforms.validators import DataRequired


class SettingsForm(FlaskForm):

    download_img = FileField('Загрузить')
    email = EmailField('Почта')
    password_last = PasswordField("Старый пароль")
    password = PasswordField('Пароль')
    password_again = PasswordField('Повторите пароль')
    name = StringField('Логин')
    bio = TextAreaField("О себе")
    submit_save = SubmitField('Сохранить')
    submit_reset = SubmitField('Сбросить')
    message = str()
    path_avatar = '/static/images/right.png'

    def set_form(self, user, message=''):
        #  self.path_avatar.data = user.image
        self.email.data = user.email
        self.name.data = user.name
        self.bio.data = 'zdes poka nichego net :('
        #  self.bio.data = user.description
        self.message = message
        self.password_last.data = None
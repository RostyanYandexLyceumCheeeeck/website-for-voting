from flask_wtf import FlaskForm
from wtforms import TextAreaField
from datetime import datetime


class ProfileForm(FlaskForm):
    bio = TextAreaField("О себе")
    name = str()
    image = '/static/images/right.png'
    created_date = None
    tests = list()

    def set_form(self, user):
        self.name = user.name
        self.bio.data = user.description
        self.image = user.image
        self.created_date = "На сайте с \n" + datetime.strftime(user.created_date, "%A,%d %B, %Y")
        self.tests = [x.to_dict() for x in user.tests[-1:-3:-1]]

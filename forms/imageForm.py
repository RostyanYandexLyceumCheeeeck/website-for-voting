from flask_wtf import FlaskForm
from wtforms import MultipleFileField, SubmitField


class ImageForm(FlaskForm):
    images = MultipleFileField('Select Images')
    submit = SubmitField('Submit')

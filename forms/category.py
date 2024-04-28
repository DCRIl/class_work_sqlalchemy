from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    name = StringField('Название Категории')
    submit = SubmitField('Применить')
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class DepartmentsForm(FlaskForm):
    title = StringField('Department title', validators=[DataRequired()])
    chief = TextAreaField("Chief")
    members = TextAreaField("Members")
    email = EmailField("Department Email")
    submit = SubmitField('Submit')
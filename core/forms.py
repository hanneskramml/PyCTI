from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    name = StringField('CTI Name: ', validators=[DataRequired()])
    submit = SubmitField('create')

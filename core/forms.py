from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()], render_kw={"placeholder": "Type name here..."})
    submit = SubmitField('Create CTI')

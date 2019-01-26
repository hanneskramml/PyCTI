from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()], render_kw={"placeholder": "Type name here..."})
    submit = SubmitField('Create CTI')


class EventsForm(FlaskForm):
    path = StringField('Path: ', validators=[], render_kw={"placeholder": "/var/log"})
    file = StringField('File: ', validators=[], render_kw={"placeholder": "events.log"})
    time = DateTimeField('Date/Time frame: ', validators=[])

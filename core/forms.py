from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()], render_kw={"placeholder": "Type name here..."})
    submit = SubmitField('Create CTI')


class EventsForm(FlaskForm):
    path = StringField('Path: ', validators=[], render_kw={"placeholder": "/home/pycti/test"})
    file = FileField('File: ', validators=[])
    limit = IntegerField('Limit (newest events): ', validators=[], render_kw={"placeholder": "10000"})
    host = StringField('Host: ', validators=[], render_kw={"placeholder": "localhost", "readonly": "True"})
    db = StringField('DB: ', validators=[], render_kw={"placeholder": "suricata", "readonly": "True"})

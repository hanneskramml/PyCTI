from core import db


class CTI(db.Model):
    __tablename__ = 'cti'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    events = db.relationship("Event")

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<CTI {}>'.format(self.id)

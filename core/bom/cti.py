from core import db

CTI_STATUS = {'NEW': 0, 'CLASSIFIED': 1, 'SHARED': 2}


class CTI(db.Model):
    __tablename__ = 'cti'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.Integer)
    events = db.relationship("Event")

    def __init__(self, name=None):
        self.name = name
        self.status = CTI_STATUS['NEW']

    def __repr__(self):
        return '<CTI {}>'.format(self.id)

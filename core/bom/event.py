from core import db


class Event(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime,  default=db.func.current_timestamp())


class NetworkEvent(Event):
    signature = db.Column(db.String)

    def __repr__(self):
        return '<NetworkEvent {}>'.format(self.id)
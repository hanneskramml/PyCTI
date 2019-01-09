from core import db

CTI_STATUS = {'NEW': 0, 'ANALYSED': 1, 'CLASSIFIED': 2, 'SHARED': 3}

mtm_cti_actor = db.Table('mtm_cti_actor',
                              db.Column('cti.id', db.Integer, db.ForeignKey('cti.id'), primary_key=True),
                              db.Column('actor.id', db.Integer, db.ForeignKey('actor.id'), primary_key=True))


class CTI(db.Model):
    __tablename__ = 'cti'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.Integer)

    events = db.relationship("Event")
    classified_actors = db.relationship("Actor", secondary=mtm_cti_actor,
                                        backref=db.backref('cti', lazy=True))

    def __init__(self, name=None):
        self.name = name
        self.status = CTI_STATUS['NEW']

    def __repr__(self):
        return '<CTI {}>'.format(self.id)

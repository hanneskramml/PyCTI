from core import db


class Event(db.Model):
    __tablename__ = 'event_base'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime)
    source_module = db.Column(db.String)

    event_type = db.Column(db.String)
    __mapper_args__ = {'polymorphic_on': event_type}

    cti = db.relationship("CTI", uselist=False)
    cti_id = db.Column(db.Integer, db.ForeignKey('cti.id'), nullable=False)

    def __init__(self, source_module, timestamp=db.func.current_timestamp()):
        self.timestamp = timestamp
        self.source_module = source_module

    def __repr__(self):
        return '<Event {}>'.format(self.id)


class NetworkEvent(Event):
    __tablename__ = 'event_network'

    event_id = db.Column(db.Integer, db.ForeignKey('event_base.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'network', 'inherit_condition': (event_id == Event.id)}

    src_ip = db.Column(db.String)
    dest_ip = db.Column(db.String)
    protocol = db.Column(db.String)
    src_port = db.Column(db.Integer)
    dest_port = db.Column(db.Integer)
    payload = db.Column(db.String)
    signature = db.Column(db.String)

    def __init__(self, source_module, timestamp=db.func.current_timestamp(), src_ip=None, dest_ip=None, protocol=None, src_port=None, dest_port=None, payload=None, signature=None):
        super(NetworkEvent, self).__init__(source_module, timestamp)
        self.src_ip = src_ip
        self.dest_ip = dest_ip
        self.protocol = protocol
        self.src_port = src_port
        self.dest_port = dest_port
        self.payload = payload
        self.signature = signature


    def __repr__(self):
        return '<NetworkEvent {}>'.format(self.id)


class HostEvent(Event):
    __tablename__ = 'event_host'

    event_id = db.Column(db.Integer, db.ForeignKey('event_base.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'host', 'inherit_condition': (event_id == Event.id)}

    file = db.Column(db.String)

    def __init__(self, source_module):
        super(HostEvent, self).__init__(source_module)

    def __repr__(self):
        return '<HostEvent {}>'.format(self.id)

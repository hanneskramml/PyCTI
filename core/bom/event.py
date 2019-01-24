from core import db

mtm_feature_event = db.Table('mtm_feature_event',
                             db.Column('feature_id', db.Integer, db.ForeignKey('feature.id'), primary_key=True),
                            db.Column('event_base_id', db.Integer, db.ForeignKey('event_base.id'), primary_key=True))


class Event(db.Model):
    __tablename__ = 'event_base'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime)
    source_module = db.Column(db.String)

    event_type = db.Column(db.String)
    __mapper_args__ = {'polymorphic_on': event_type}

    cti = db.relationship("CTI", uselist=False, lazy=True)
    cti_id = db.Column(db.Integer, db.ForeignKey('cti.id'), nullable=False)

    analysed_features = db.relationship('Feature', secondary=mtm_feature_event,
                                        backref=db.backref('events', lazy=True), lazy=True)

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
    reference = db.Column(db.String)

    def __init__(self, source_module, timestamp=db.func.current_timestamp(), src_ip=None, dest_ip=None, protocol=None, src_port=None, dest_port=None, payload=None, signature=None, reference=None):
        super(NetworkEvent, self).__init__(source_module, timestamp)
        self.src_ip = src_ip
        self.dest_ip = dest_ip
        self.protocol = protocol
        self.src_port = src_port
        self.dest_port = dest_port
        self.payload = payload
        self.signature = signature
        self.reference = reference

    def __repr__(self):
        return '<NetworkEvent {}>'.format(self.id)


class HostEvent(Event):
    __tablename__ = 'event_host'

    event_id = db.Column(db.Integer, db.ForeignKey('event_base.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'host', 'inherit_condition': (event_id == Event.id)}

    file = db.Column(db.String)
    content = db.Column(db.String)
    signature = db.Column(db.String)

    def __init__(self, source_module, timestamp=db.func.current_timestamp(), file=None, content=None, signature=None):
        super(HostEvent, self).__init__(source_module, timestamp)
        self.file = file
        self.content = content
        self.signature = signature

    def __repr__(self):
        return '<HostEvent {}>'.format(self.id)


class GenericEvent(Event):
    __tablename__ = 'event_generic'

    event_id = db.Column(db.Integer, db.ForeignKey('event_base.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'generic', 'inherit_condition': (event_id == Event.id)}

    content = db.Column(db.String)

    def __init__(self, source_module, timestamp=db.func.current_timestamp(), content=None):
        super(GenericEvent, self).__init__(source_module, timestamp)
        self.content = content

    def __repr__(self):
        return '<GenericEvent {}>'.format(self.id)
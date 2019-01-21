from core import db

mtm_actor_software = db.Table('mtm_actor_software',
                              db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True),
                              db.Column('software_id', db.Integer, db.ForeignKey('software.id'), primary_key=True))

mtm_actor_behaviour = db.Table('mtm_actor_behaviour',
                              db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True),
                              db.Column('behaviour_id', db.Integer, db.ForeignKey('behaviour.id'), primary_key=True))

mtm_behaviour_software = db.Table('mtm_behaviour_software',
                              db.Column('behaviour_id', db.Integer, db.ForeignKey('behaviour.id'), primary_key=True),
                              db.Column('software_id', db.Integer, db.ForeignKey('software.id'), primary_key=True))

mtm_behaviour_phase = db.Table('mtm_behaviour_phase',
                              db.Column('behaviour_id', db.Integer, db.ForeignKey('behaviour.id'), primary_key=True),
                              db.Column('phase_id', db.Integer, db.ForeignKey('phase.id'), primary_key=True))


class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ext_id = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    alias = db.Column(db.String)
    description = db.Column(db.String)

    uses_software = db.relationship('Software', secondary=mtm_actor_software, lazy='subquery')
    uses_behaviours = db.relationship('Behaviour', secondary=mtm_actor_behaviour, lazy='subquery')

    def __init__(self, ext_id=None, name=None, alias=None, description=None):
        self.ext_id = ext_id
        self.name = name
        self.alias = alias
        self.description = description

    def __repr__(self):
        return '<Actor {}>'.format(self.id)


class Feature(db.Model):
    __tablename__ = 'feature'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ext_id = db.Column(db.String, unique=True)
    name = db.Column(db.String, index=True)
    description = db.Column(db.String)
    power = db.Column(db.Float)

    feat_type = db.Column(db.String)
    __mapper_args__ = {'polymorphic_on': feat_type}

    def __init__(self, extId=None, name=None, description=None, power=1):
        self.ext_id = extId
        self.name = name
        self.description = description
        self.power = power

    def __eq__(self, other):
        return self.name == other

    def __repr__(self):
        return '<Feature {}>'.format(self.id)


class Software(Feature):
    __tablename__ = 'software'

    id = db.Column(db.Integer, db.ForeignKey('feature.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'software', 'inherit_condition': (id == Feature.id)}

    type = db.Column(db.String)
    alias = db.Column(db.String)
    platforms = db.Column(db.String)

    usedby_actors = db.relationship('Actor', secondary=mtm_actor_software, lazy=True)
    usedby_behaviours = db.relationship('Behaviour', secondary=mtm_behaviour_software, lazy=True)

    def __init__(self, extId=None, name=None, description=None, type=None, alias=None, platforms=None):
        super(Software, self).__init__(extId, name, description)
        self.type = type
        self.alias = alias
        self.platforms = platforms

    def __repr__(self):
        return '<Software {}>'.format(self.id)


class Behaviour(Feature):
    __tablename__ = 'behaviour'

    id = db.Column(db.Integer, db.ForeignKey('feature.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'behaviour', 'inherit_condition': (id == Feature.id)}

    platforms = db.Column(db.String)
    mitigations = db.Column(db.String)

    uses_software = db.relationship('Software', secondary=mtm_behaviour_software, lazy=True)
    usedby_actors = db.relationship('Actor', secondary=mtm_actor_behaviour, lazy=True)
    phases = db.relationship('Phase', secondary=mtm_behaviour_phase, lazy=True)

    def __init__(self, extId=None, name=None, description=None, platforms=None, mitigations=None):
        super(Behaviour, self).__init__(extId, name, description)
        self.platforms = platforms
        self.mitigations = mitigations

    def __repr__(self):
        return '<Behaviour {}>'.format(self.id)


class Phase(db.Model):
    __tablename__ = 'phase'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ext_id = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    behaviours = db.relationship('Behaviour', secondary=mtm_behaviour_phase, lazy=True)

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Phase {}>'.format(self.id)

from core import db

mtm_actor_software = db.Table('mtm_actor_software',
                              db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True),
                              db.Column('software_id', db.Integer, db.ForeignKey('software.id'), primary_key=True))

mtm_actor_technique = db.Table('mtm_actor_technique',
                              db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True),
                              db.Column('technique_id', db.Integer, db.ForeignKey('technique.id'), primary_key=True))

mtm_technique_software = db.Table('mtm_technique_software',
                              db.Column('technique_id', db.Integer, db.ForeignKey('technique.id'), primary_key=True),
                              db.Column('software_id', db.Integer, db.ForeignKey('software.id'), primary_key=True))

mtm_technique_tactic = db.Table('mtm_technique_tactic',
                              db.Column('technique_id', db.Integer, db.ForeignKey('technique.id'), primary_key=True),
                              db.Column('tactic_id', db.Integer, db.ForeignKey('tactic.id'), primary_key=True))


class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ext_id = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    alias = db.Column(db.String)

    uses_software = db.relationship('Software', secondary=mtm_actor_software, lazy='subquery')
    uses_techniques = db.relationship('Technique', secondary=mtm_actor_technique, lazy='subquery')

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Actor {}>'.format(self.id)


class Software(db.Model):
    __tablename__ = 'software'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ext_id = db.Column(db.String, unique=True)
    name = db.Column(db.String)

    usedby_actors = db.relationship('Actor', secondary=mtm_actor_software, lazy=True)
    usedby_techniques = db.relationship('Technique', secondary=mtm_technique_software, lazy=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Software {}>'.format(self.id)


class Technique(db.Model):
    __tablename__ = 'technique'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ext_id = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    uses_software = db.relationship('Software', secondary=mtm_technique_software, lazy=True)
    usedby_actors = db.relationship('Actor', secondary=mtm_actor_technique, lazy=True)
    tactics = db.relationship('Tactic', secondary=mtm_technique_tactic, lazy=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Technique {}>'.format(self.id)


class Tactic(db.Model):
    __tablename__ = 'tactic'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ext_id = db.Column(db.String, unique=True)
    name = db.Column(db.String)

    techniques = db.relationship('Technique', secondary=mtm_technique_tactic, lazy=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Tactic {}>'.format(self.id)

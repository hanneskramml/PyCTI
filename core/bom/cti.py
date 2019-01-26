import json
from core import db

CTI_STATUS = {'NEW': 0, 'ANALYSED': 1, 'CLASSIFIED': 2, 'SHARED': 3, 'ARCHIVED': 4}

mtm_cti_feature = db.Table('mtm_cti_feature',
                              db.Column('cti_id', db.Integer, db.ForeignKey('cti.id'), primary_key=True),
                              db.Column('feature_id', db.Integer, db.ForeignKey('feature.id'), primary_key=True))


class CTI(db.Model):
    __tablename__ = 'cti'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.Integer)

    events = db.relationship("Event", lazy=True)
    features = db.relationship("Feature", secondary=mtm_cti_feature, backref=db.backref('cti', lazy=True))
    classifications = db.relationship("Classification")

    def __init__(self, name=None):
        self.name = name
        self.status = CTI_STATUS['NEW']

    def get_status_name(self):
        for key in CTI_STATUS:
            if self.status == CTI_STATUS[key]:
                return key

        return None

    def get_top_classification(self):
        max_prob = 0
        top_class = None

        for classification in self.classifications:
            if max_prob < classification.probability:
                max_prob = classification.probability
                top_class = classification

        return top_class

    def get_chart_data(self):
        targets = []
        probs = []
        for classification in self.classifications:
            targets.append(classification.actor.name)
            probs.append(round(classification.probability * 100, 1))

        return json.dumps({"labels": targets, "data": probs})

    def __repr__(self):
        return '<CTI {}>'.format(self.id)


class Classification(db.Model):
    __tablename__ = 'classification'

    cti_id = db.Column(db.Integer, db.ForeignKey('cti.id'), nullable=False, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), nullable=False, primary_key=True)
    source_module = db.Column(db.String(20), primary_key=True)
    probability = db.Column(db.Float)

    cti = db.relationship("CTI", uselist=False)
    actor = db.relationship("Actor", uselist=False)

    def __init__(self, source_module=None, probability=None):
        self.source_module = source_module
        self.probability = probability

    def __repr__(self):
        return '<Classification {}.{}>'.format(self.cti_id, self.actor_id)

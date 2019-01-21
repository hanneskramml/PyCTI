from flask_sqlalchemy import inspect
from core import db
from core.bom import Actor, Software, Behaviour, Feature
from core.training_data import TrainingSet

SQL_GET_FEAT_BEHAVIOURS = "SELECT b.id, b.name, COUNT(f.behaviour_id) AS feat_count FROM behaviour b LEFT OUTER JOIN (SELECT mtm.behaviour_id FROM event_base e JOIN mtm_event_behaviour mtm on e.id = mtm.event_base_id WHERE e.cti_id = :cti) f on b.id == f.behaviour_id GROUP BY b.id, b.name ORDER BY b.id"
SQL_GET_FEAT_SOFTWARE = "SELECT s.id, s.name, s.type, COUNT(f.software_id) AS feat_count FROM software s LEFT OUTER JOIN (SELECT mtm.software_id FROM event_base e JOIN mtm_event_software mtm on e.id = mtm.event_base_id WHERE e.cti_id = :cti) f on s.id = f.software_id GROUP BY s.id, s.name, s.type ORDER BY s.id"
SQL_TRAIN_FEAT_BEHAVIOURS = "SELECT b.id, b.name, COUNT(f.behaviour_id) AS feat_count FROM behaviour b LEFT OUTER JOIN (SELECT mtm.behaviour_id FROM actor a JOIN mtm_actor_behaviour mtm on a.id = mtm.actor_id WHERE a.id = :actor) f on b.id = f.behaviour_id GROUP BY b.id, b.name ORDER BY b.id"
SQL_TRAIN_FEAT_SOFTWARE = "SELECT s.id, s.name, s.type, COUNT(f.software_id) AS feat_count FROM software s LEFT OUTER JOIN (SELECT mtm.software_id FROM actor a JOIN mtm_actor_software mtm on a.id = mtm.actor_id WHERE a.id = :actor) f on s.id = f.software_id GROUP BY s.id, s.name, s.type ORDER BY s.id"


def get_dict_from_object(obj):
    return {column.key: getattr(obj, column.key)
            for column in inspect(obj).mapper.column_attrs}


def get_features_from_cti(cti):

    features = {feature.name: feature.power for feature in db.session.query(Feature).order_by(Feature.feat_type, Feature.id).all()}
    feat_vector = []

    rs = db.engine.execute(SQL_GET_FEAT_BEHAVIOURS, {'cti': cti.id})
    for row in rs:
        if row.feat_count == 0:
            feat_vector.append(0)
        elif row.feat_count > 0:
            feat_vector.append(1)
            print("Behaviour Feature: {} (Value: {})".format(row.name, row.feat_count))
        else:
            print("WARNING: unexpected feature value")


    rs = db.engine.execute(SQL_GET_FEAT_SOFTWARE, {'cti': cti.id})
    for row in rs:
        if row.feat_count == 0:
            feat_vector.append(0)
        elif row.feat_count > 0:
            if row.type == 'malware':
                feat_vector.append(1)
            else:
                feat_vector.append(0.2)

            print("Software Feature: {} (Value: {})".format(row.name, row.feat_count))
        else:
            print("WARNING: unexpected feature value")

    return [feat_vector]


def get_training_data():

    ts = TrainingSet()
    for behaviour in db.session.query(Behaviour).order_by(Behaviour.id).all():
        ts.add_feature(behaviour.name)

    for software in db.session.query(Software).order_by(Software.id).all():
        ts.add_feature(software.name)


    actors = Actor.query.order_by(Actor.id).all()
    for i in range(len(actors)):

        ts.add_sample_for_features(target=actors[i].id, target_name=actors[i].name, init_values=0)

        features = {}
        feat_sw = {}
        rs = db.engine.execute(SQL_TRAIN_FEAT_BEHAVIOURS, {'actor': actors[i].id})
        for row in rs:
            if row.feat_count > 0:
                features[row.name] = 1

        rs = db.engine.execute(SQL_TRAIN_FEAT_SOFTWARE, {'actor': actors[i].id})
        for row in rs:
            if row.feat_count > 0:
                features[row.name] = 1

        ts.add_sample_for_features(features, actors[i].id, actors[i].name)

        for key in features:
            features[key] = 0

        #features = {sw.name: 0 for sw in db.session.query(Software).filter_by(type='malware').order_by(Software.id).all()}

        for software in db.session.query(Software).filter(Software.usedby_actors.any(id=actors[i].id)).all():
            if software.type == 'malware':
                features[software.name] = 1
                ts.add_sample_for_features(features, actors[i].id, actors[i].name)
                features[software.name] = 0
            #else:
                #ts.add_sample_for_feature(software.name, 0.1, actors[i].id)

    print(ts.get_all())
    print("Number of features: {}".format(ts.n_features))
    print("Number of training samples: {}".format(ts.n_samples))

    return ts.get_all()

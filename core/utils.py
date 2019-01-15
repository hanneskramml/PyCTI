from flask_sqlalchemy import inspect
from core import db
from core.bom import Actor

SQL_GET_FEAT_BEHAVIOURS = "SELECT b.id, b.name, COUNT(f.behaviour_id) AS feat_count FROM behaviour b LEFT OUTER JOIN (SELECT mtm.behaviour_id FROM event_base e JOIN mtm_event_behaviour mtm on e.id = mtm.event_base_id WHERE e.cti_id = :cti) f on b.id == f.behaviour_id GROUP BY b.id, b.name ORDER BY b.id"
SQL_GET_FEAT_SOFTWARE = "SELECT s.id, s.name, COUNT(f.software_id) AS feat_count FROM software s LEFT OUTER JOIN (SELECT mtm.software_id FROM event_base e JOIN mtm_event_software mtm on e.id = mtm.event_base_id WHERE e.cti_id = :cti) f on s.id = f.software_id GROUP BY s.id, s.name ORDER BY s.id"
SQL_TRAIN_FEAT_BEHAVIOURS = "SELECT b.id, b.name, COUNT(f.behaviour_id) AS feat_count FROM behaviour b LEFT OUTER JOIN (SELECT mtm.behaviour_id FROM actor a JOIN mtm_actor_behaviour mtm on a.id = mtm.actor_id WHERE a.id = :actor) f on b.id = f.behaviour_id GROUP BY b.id, b.name ORDER BY b.id"
SQL_TRAIN_FEAT_SOFTWARE = "SELECT s.id, s.name, COUNT(f.software_id) AS feat_count FROM software s LEFT OUTER JOIN (SELECT mtm.software_id FROM actor a JOIN mtm_actor_software mtm on a.id = mtm.actor_id WHERE a.id = :actor) f on s.id = f.software_id GROUP BY s.id, s.name ORDER BY s.id"


def get_dict_from_object(obj):
    return {column.key: getattr(obj, column.key)
            for column in inspect(obj).mapper.column_attrs}


def get_features_from_cti(cti):
    feat_vector = []

    rs = db.engine.execute(SQL_GET_FEAT_BEHAVIOURS, {'cti': cti.id})
    for row in rs:
        feat_vector.append(row.feat_count)

    rs = db.engine.execute(SQL_GET_FEAT_SOFTWARE, {'cti': cti.id})
    for row in rs:
        feat_vector.append(row.feat_count)

    return feat_vector


def get_training_data():
    training_vector = {'features': [], 'target': []}

    actors = Actor.query.order_by(Actor.id).all()
    for actor in actors:
        features = []

        rs = db.engine.execute(SQL_TRAIN_FEAT_BEHAVIOURS, {'actor': actor.id})
        for row in rs:
            features.append(row.feat_count)

        rs = db.engine.execute(SQL_TRAIN_FEAT_SOFTWARE, {'actor': actor.id})
        for row in rs:
            features.append(row.feat_count)

        training_vector['features'].append(features)
        training_vector['target'].append(actor.id)

    return training_vector

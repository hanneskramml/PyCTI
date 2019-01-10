from flask_sqlalchemy import inspect
from core import db

SQL_FEAT_BEHAVIOURS_VIEW = "SELECT b.id, b.name, COUNT(f.behaviour_id) AS feat_count FROM behaviour b LEFT OUTER JOIN (SELECT mtm.behaviour_id FROM event_base e JOIN mtm_event_behaviour mtm on e.id = mtm.event_base_id WHERE e.cti_id = :cti) f on id == f.behaviour_id GROUP BY b.id, b.name ORDER BY b.id"
SQL_FEAT_SOFTWARE_VIEW = "SELECT s.id, s.name, COUNT(f.software_id) AS feat_count FROM software s LEFT OUTER JOIN (SELECT mtm.software_id FROM event_base e JOIN mtm_event_software mtm on e.id = mtm.event_base_id WHERE e.cti_id = :cti) f on s.id = f.software_id GROUP BY s.id, s.name ORDER BY s.id"

def get_dict_from_object(obj):
    return {column.key: getattr(obj, column.key)
            for column in inspect(obj).mapper.column_attrs}


def vectorize_features(cti):

    vector = []
    rs = db.engine.execute(SQL_FEAT_BEHAVIOURS_VIEW, {'cti': cti.id})
    for row in rs:
        vector.append(row.feat_count)

    rs = db.engine.execute(SQL_FEAT_SOFTWARE_VIEW, {'cti': cti.id})
    for row in rs:
        vector.append(row.feat_count)

    return vector

import json

from stix2 import FileSystemSource, Filter, utils
from itertools import chain
from core.bom.baseline import *
from core import db
from config import Config


class MitreKnowledgeBase:

    fs = FileSystemSource(Config.REPO_PATH + '/mitre/enterprise-attack')
    relations = None

    @classmethod
    def __get__all_actors(cls):
        filter = [Filter('type', '=', 'intrusion-set')]
        return cls.fs.query(filter)

    @classmethod
    def __get_all_techniques(cls):
        filter = [Filter('type', '=', 'attack-pattern')]
        return cls.fs.query(filter)

    @classmethod
    def __get_all_software(cls):
        filter = [
            [Filter('type', '=', 'malware')],
            [Filter('type', '=', 'tool')]
        ]
        return list(chain.from_iterable(
            cls.fs.query(f) for f in filter
        ))

    @classmethod
    def __get_mitigation_by_id(cls, id):
        filter = [
            Filter('type', '=', 'course-of-action'),
            Filter('id', '=', id)
        ]
        return cls.fs.query(filter)

    @classmethod
    def __find_relationships(cls, rel_type=None, source_id=None, target_id=None):
        if cls.relations is None:
            cls.relations = cls.fs.query([
                Filter('type', '=', 'relationship')
            ])

        relations = []
        for rel in cls.relations:
            if rel_type is None or rel_type == rel.relationship_type:
                if source_id is None or source_id == rel.source_ref:
                    if target_id is None or target_id == rel.target_ref:
                        relations.append(rel)

        return relations

    @classmethod
    def load_baseline(cls):

        print("Loading baseline from MITRE. This may take some time...")
        for act in cls.__get__all_actors():
            actor = Actor(ext_id=act.id, name=act.name)

            if "aliases" in act:
                actor.alias = json.dumps(act['aliases'])

            if "description" in act:
                actor.description = act.description

            db.session.add(actor)

        for tec in cls.__get_all_techniques():
            behaviour = Behaviour(extId=tec.id, name=tec.name)

            if "description" in tec:
                behaviour.description = tec.description

            if "x_mitre_platforms" in tec:
                behaviour.platforms = json.dumps(tec['x_mitre_platforms'])

            for rel in cls.__find_relationships(target_id=tec.id, rel_type='mitigates'):
                mitigation = cls.__get_mitigation_by_id(rel.source_ref)
                behaviour.mitigation_name = mitigation[0].name
                behaviour.mitigation_desc = mitigation[0].description

            db.session.add(behaviour)

        for sw in cls.__get_all_software():
            software = Software(extId=sw.id, name=sw.name, type=sw.type)

            if "description" in sw:
                software.description = sw.description
            if "x_mitre_aliases" in sw:
                software.alias = json.dumps(sw['x_mitre_aliases'])
            if "x_mitre_platforms" in sw:
                software.platforms = json.dumps(sw['x_mitre_platforms'])

            db.session.add(software)

        for actor in Actor.query.all():
            #print("MITRE: Setting relationships for actor {}...".format(actor.name))
            for rel in cls.__find_relationships(source_id=actor.ext_id, rel_type='uses'):
                type = utils.get_type_from_id(rel.target_ref)

                if type in ['attack-pattern']:
                    behaviour = Behaviour.query.filter_by(ext_id=rel.target_ref).first()
                    actor.uses_behaviours.append(behaviour)
                elif type in ['malware', 'tool']:
                    software = Software.query.filter_by(ext_id=rel.target_ref).first()
                    actor.uses_software.append(software)

            db.session.add(actor)

        db.session.commit()
        print("Successfully loaded baseline from MITRE Att&ck knowledge base")

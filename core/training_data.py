import numpy as np
from core.bom import Feature, Actor, Behaviour, Software


class TrainingSet(object):

    def __init__(self):

        self.n_features = 0
        self.n_samples = 0

        self.feature_names = []
        self.target_names = []

        self.__features = []
        self.__target = []

    def __getattr__(self, key):
        if key == 'features':
            return np.asarray(self.__features, dtype=np.float64)
        elif key == 'target':
            return np.asarray(self.__target, dtype=np.int)
        raise AttributeError(key)

    def add_feature(self, feature_name):
        self.feature_names.append(feature_name)
        self.n_features += 1

    def add_sample(self, features, target, target_name=None):
        self.__features.append(features)
        self.__target.append(target)
        self.target_names.append(target_name)
        self.n_samples += 1

    def add_samples(self, feature_list, targets, target_names=None):
        if len(feature_list) != len(targets) or len(feature_list) != len(target_names):
            raise Exception

        for i in range(len(feature_list)):
            self.add_sample(feature_list[i], targets[i], target_names[i])

    def add_sample_for_features(self, features=None, target=None, target_name=None, init_values=-1):
        feat_vector = self.get_vector_from_features(features=features, init_values=init_values)
        self.add_sample(feat_vector, target, target_name)

    def get_vector_from_features(self, features=None, init_values=0):
        feat_vector = [init_values for x in range(self.n_features)]

        if features is None:
            features = {}
        for key in features:
            index = self.feature_names.index(key)
            feat_vector[index] = features[key]

        return feat_vector

    def init_from_db(self):
        for feature in Feature.query.order_by(Feature.feat_type, Feature.id).all():
            self.add_feature(feature.name)

        for actor in Actor.query.order_by(Actor.id).all():
            self.add_sample_for_features(target=actor.id, target_name=actor.name, init_values=0)

            features = {}
            for behaviour in Behaviour.query.filter(Behaviour.usedby_actors.any(id=actor.id)).all():
                features[behaviour.name] = 1

            software_rs = Software.query.filter(Software.usedby_actors.any(id=actor.id)).all()
            for software in software_rs:
                features[software.name] = 1

            self.add_sample_for_features(features=features, target=actor.id, target_name=actor.name)

            for key in features:
                features[key] = 0

            for software in software_rs:
                if software.type == 'malware':
                    features[software.name] = 1
                    self.add_sample_for_features(features=features, target=actor.id, target_name=actor.name)
                    features[software.name] = 0

        print(self.get_data())
        print("Number of features: {}".format(self.n_features))
        print("Number of training samples: {}".format(self.n_samples))

    def get_data(self):
        return {'features': self.features, 'feature_names': self.feature_names,
                'target': self.target, 'target_names': self.target_names}

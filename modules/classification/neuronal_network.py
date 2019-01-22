from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from core import ts
from modules.classification import ClassificationModule


class NeuronalNetwork(ClassificationModule):

    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes = (258, ), random_state = 1, activation='logistic')
    scaler = StandardScaler()

    @classmethod
    def train_algorithm(cls, training_set):
        cls.scaler.fit(training_set['features'])
        cls.clf.fit(cls.__standardize_features(training_set['features']), training_set['target'])

    @classmethod
    def classify_features(cls, features):
        feat_standardized = cls.__standardize_features(features)
        return cls.clf.predict(feat_standardized), cls.clf.predict_proba(feat_standardized)

    @classmethod
    def __standardize_features(cls, features):
        return cls.scaler.transform(features)
        #return features


if ts.n_samples > 0:
    training_set = ts.get_data()
    NeuronalNetwork.train_algorithm(training_set)
    print("Algorithm trained (NeuronalNetwork)")

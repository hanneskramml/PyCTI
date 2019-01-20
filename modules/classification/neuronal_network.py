from sklearn.neural_network import MLPClassifier
from core import ts
from modules.classification import ClassificationModule


class NeuronalNetwork(ClassificationModule):

    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes = (258, ), random_state = 1, activation='logistic')

    @classmethod
    def train_algorithm(cls, training_set):
        cls.clf.fit(training_set['features'], training_set['target'])

    @classmethod
    def classify_features(cls, features):
        return cls.clf.predict(features), cls.clf.predict_proba(features)


if ts.n_samples > 0:
    training_set = ts.get_data()
    NeuronalNetwork.train_algorithm(training_set)
    print("Algorithm trained (NeuronalNetwork)")

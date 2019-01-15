from sklearn.tree import DecisionTreeClassifier
from core import utils
from modules.classification import ClassificationModule


class DecisionTree(ClassificationModule):

    tree = DecisionTreeClassifier()

    @classmethod
    def train_algorithm(cls, data):
        cls.tree = cls.tree.fit(data['features'], data['target'])

    @classmethod
    def classify_features(cls, features):
        return cls.tree.predict([features])


data = utils.get_training_data()
DecisionTree.train_algorithm(data)
print("Algorithm trained (DecisionTree)")

from sklearn import tree
#import graphviz as graphviz

from core import ts
from modules.classification import ClassificationModule


class DecisionTree(ClassificationModule):

    clf = tree.DecisionTreeClassifier()

    @classmethod
    def train_algorithm(cls, training_set):
        cls.clf = cls.clf.fit(training_set['features'], training_set['target'])

        #dot_data = tree.export_graphviz(cls.clf, out_file=None, feature_names=training_set['feature_names'], class_names=training_set['target_names'])
        #graph = graphviz.Source(dot_data)
        #graph.render("decision_tree")

    @classmethod
    def classify_features(cls, features):
        return cls.clf.predict(features), cls.clf.predict_proba(features)


if ts.n_samples > 0:
    training_set = ts.get_data()
    DecisionTree.train_algorithm(training_set)
    print("Algorithm trained (DecisionTree)")

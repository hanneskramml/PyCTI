from flask import Blueprint

bp = Blueprint('classification', __name__)


class ClassificationModule(object):

    @classmethod
    def train_algorithm(cls, training_set):
        raise NotImplementedError

    @classmethod
    def classify_features(cls, features):
        raise NotImplementedError


from modules.classification import classification_handler

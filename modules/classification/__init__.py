from flask import Blueprint

bp = Blueprint('classification', __name__)


class ClassificationModule(object):

    @classmethod
    def classify_features(cls, features):
        raise NotImplementedError

    @classmethod
    def train_algorithm(cls, data):
        raise NotImplementedError


from modules.classification import classification_handler

from flask import Blueprint

bp = Blueprint('classification', __name__)


class ClassificationModule(object):

    @classmethod
    def classify_cti(cls, cti):
        raise NotImplementedError

    @classmethod
    def train_algorithm(cls):
        raise NotImplementedError


from modules.classification import classification_handler

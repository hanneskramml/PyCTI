from flask import Blueprint

bp = Blueprint('input', __name__)


class InputModule(object):

    @classmethod
    def get_events(cls, path):
        raise NotImplementedError

    @classmethod
    def run_scan(cls, path):
        raise NotImplementedError


from modules.input import input_handler


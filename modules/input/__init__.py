import os
from flask import Blueprint

templates_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
bp = Blueprint('input', __name__, template_folder = templates_folder)


class InputModule(object):

    @classmethod
    def get_events(cls, path, file):
        raise NotImplementedError

    @classmethod
    def run_scan(cls, path):
        raise NotImplementedError


from modules.input import input_handler


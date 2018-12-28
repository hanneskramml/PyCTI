from flask import Blueprint
from importlib import import_module
from core import app

bp = Blueprint('input', __name__)

for input_module in app.config['INPUT_MODULES']:
    import_module('.' + input_module, __name__)

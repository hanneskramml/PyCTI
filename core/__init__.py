from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
nav = Nav(app)

from modules.input import bp as input_bp
app.register_blueprint(input_bp)

from core import bom, navigation, routes
db.create_all()

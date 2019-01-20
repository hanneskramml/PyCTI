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

from core import bom
if Config.CREATE_DB_AND_INIT_BASELINE:
    db.create_all()
    from baseline_loader import MitreKnowledgeBase
    MitreKnowledgeBase.load_baseline()

from .rule_manager import RuleManager
rulemanager = RuleManager(rulepath=Config.YARA_RULE_PATH)

from .training_data import TrainingSet
ts = TrainingSet()
ts.init_from_db()

from modules.input import bp as input_bp
app.register_blueprint(input_bp, url_prefix='/input')

from modules.classification import bp as classification_bp
app.register_blueprint(classification_bp, url_prefix='/classify')

from core import navigation, controller
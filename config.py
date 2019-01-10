import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLITE_DB_PATH = os.path.join(base_dir, 'db.sqlite3')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQLITE_DB_PATH
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_SERVE_LOCAL = True
    YARA_RULE_PATH = os.path.join(base_dir, 'rules')
    REPO_PATH = os.path.join(base_dir, 'repos')
    CREATE_DB_AND_INIT_BASELINE = True if not os.path.isfile(SQLITE_DB_PATH) else False

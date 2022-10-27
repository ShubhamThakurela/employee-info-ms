from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from .config.config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


# def create_app(config_name):
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_object(config_by_name[config_name])
#     db.init_app(app)
#     flask_bcrypt.init_app(app)
#
#     return app
# ### Working Currently for === "SECRET_KEY is used by Flask and extensions to keep data safe.
# It’s set to 'dev' to provide a convenient value during development,
# but it should be overridden with a random value when deploying.
# DATABASE is the path where the SQLite database file will be saved.
# It’s under app.instance_path, which is the path that Flask has chosen
# for the instance folder. You’ll learn more about the database in the next section.""

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app

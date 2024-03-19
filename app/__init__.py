import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
# import flask migrate here
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
# Instantiate Flask-Migrate library here
migrate = Migrate(app, db)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'properties')

from app import views, models
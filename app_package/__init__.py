from flask import Flask
from app_package.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate #migrate creates migrate script which would make db modifications easier
from flask_pymongo import PyMongo
from flask_login import LoginManager
from app_package.config import Config

#object creations from line 9 to 14
app=Flask(__name__)
app.config.from_object(Config)
db=SQLAlchemy(app) #db object is created
migrate=Migrate(app,db)
mongo=PyMongo(app)

login_manager=LoginManager(app)
login_manager.login_view="index"

from app_package import routes, models

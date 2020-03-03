import os

base_dir=os.path.abspath(os.path.dirname(__file__)) #this will give absolute path(../04_flask/../app_package..) of the application(app_package)
class Config(object):
    SECRET_KEY=os.urandom(24).hex()
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://flaskuser:flaskuser@localhost/userdb"#this is the db URI
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    MONGO_URI="mongodb://localhost:27017/empdb"
    

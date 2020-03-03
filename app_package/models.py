from app_package import db,login_manager
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256 as pbsha
#from werkzeug.security generate_password_hash

@login_manager.user_loader
def load_user(id):#its used for login_manager
    return User.query.get(id)
class User(UserMixin,db.Model):#User is a modelname/object
    id=db.Column(db.Integer, primary_key=True)#its autoincremented
    username=db.Column(db.String(64), unique=True)
    password_hash=db.Column(db.String(128))
    
    def set_password(self,password):
        self.password_hash=pbsha.hash(password)
        
    def check_password(self,password):
        return pbsha.verify(password,self.password_hash)
      

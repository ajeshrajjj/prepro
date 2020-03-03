from flask_wtf import  FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired,EqualTo,ValidationError  
from app_package.models import User

class LoginForm(FlaskForm):
    username=StringField("Username: ",validators=[DataRequired()])
    password=PasswordField("Password: ",validators=[DataRequired()])
    remember_me=BooleanField("Remember Me: ")
    submit=SubmitField("Sign in: ")


class RegistrationForm(FlaskForm):
    username=StringField("Username: ",validators=[DataRequired()])
    password=PasswordField("Password: ",validators=[DataRequired()])
    password2=PasswordField("ReEnter Password: ",validators=[DataRequired(),EqualTo("password")])
    submit=SubmitField("Sign in: ")
    
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username exists, choose another one")   


class AddEmployeeForm(FlaskForm):
    name=StringField("Name: ",validators=[DataRequired()])
    age=IntegerField("Age: ",validators=[DataRequired()])
    ed=StringField("Education: ",validators=[DataRequired()])
    role=StringField("Role: ",validators=[DataRequired()])
    submit=SubmitField("Add Employee: ")
class DeleteEmployeeForm(FlaskForm):
    id=IntegerField("Id of the employee to be deleted: ",validators=[DataRequired()]) 
    submit=SubmitField("Delete Employee: ")
class ModifyEmployeeForm(FlaskForm):
    id=IntegerField("Id of the employee to be modified: ",validators=[DataRequired()])
    ed=StringField("Education: ")
    role=StringField("Role: ")
    submit=SubmitField("Modify Employee: ")
    

from flask import render_template, flash, redirect, url_for #flash is to provide any message to user and the redirect is to redirect to a different URL
from app_package import app,db,mongo
from flask_login import current_user, login_user, logout_user, login_required
from app_package.forms import LoginForm, RegistrationForm, AddEmployeeForm, DeleteEmployeeForm, ModifyEmployeeForm
from app_package.models import User

emp_id=0 #globally declaring an id
@app.route("/",methods=["GET","POST"])#ideally, use post, because get reveals data in links
def index():
    if current_user.is_authenticated:
        return redirect(url_for("menu"))
    else:
        form=LoginForm()
        if form.validate_on_submit():
            user=User.query.filter_by(username=form.username.data).first() 
            if user is None or not user.check_password(form.password.data):
                flash("invalid user")
                return redirect(url_for("index"))
            else:
                login_user(user,remember=form.remember_me.data)
                return redirect(url_for("menu"))
        else:
            return render_template("login.html",form=form) 
@app.route("/register",methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("menu"))
    else:
        form=RegistrationForm()
        if form.validate_on_submit():
            user=User(username=form.username.data)
            user.set_password(form.password.data) #now, data is created
            db.session.add(user) #now data is added to db
            db.session.commit()
            flash("User Registered..You may login")
            return redirect(url_for("index"))
        else:
            return render_template("register.html",form=form)      
            
@app.route("/menu")
@login_required
def menu():
    return render_template("menu.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))          

@app.route("/add_employee",methods=["GET","POST"])   
@login_required          
def add_employee():
    global emp_id #instatiation the globally declared variable inside the def
    form=AddEmployeeForm()
    if form.validate_on_submit():
        fields=["_id","name","age","ed","role"]
        emp_id+=1
        values=[emp_id,form.name.data,form.age.data,form.ed.data,form.role.data]
        employee=dict(zip(fields,values))
        emp_col=mongo.db.employees#here 'mongo' is a variable which we have created which comes with an attirute,'db' ...we are calling the collection as 'employees' 
        tmp=emp_col.insert_one(employee)
        if tmp.inserted_id==emp_id:
            flash("Employee added")
            return redirect(url_for("menu"))
        else:
            flash("Problem adding employee")
            return redirect(url_for("logout"))
    else:
        return render_template("add_employee.html",form=form)

@app.route("/delete_employee",methods=["GET","POST"])
@login_required
def delete_employee():
    form=DeleteEmployeeForm()
    if form.validate_on_submit():
        emp_col=mongo.db.employees
        query={"_id":form.id.data}
        emp_col.delete_one(query)
        flash("Employee deleted")
        return redirect(url_for("menu"))
    else:
        return render_template("delete_employee.html",form=form)
    
@app.route("/modify_employee",methods=["GET","POST"])
@login_required
def modify_employee():
    form=ModifyEmployeeForm()
    if form.validate_on_submit():#here both query and values needs to be passed (which may be of role or ed or both)
        values=dict()
        if form.ed.data!="":values["ed"]=form.ed.data#if ed not empty add it to values
        if form.role.data!="":values["role"]=form.role.data#if role not empty add it to values
        new_data={"$set":values}
        query={"_id":form.id.data}
        emp_col=mongo.db.employees
        emp_col.update_one(query,new_data)
        flash("Employee modified")
        return redirect(url_for("menu"))
    else:
        return render_template("modify_employee.html",form=form)

@app.route("/display_employees")
@login_required
def display_employees():
    emp_col=mongo.db.employees
    employees=emp_col.find()
    return render_template("display_employees.html",employees=employees)
    
        



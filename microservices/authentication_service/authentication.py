from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from sqlalchemy import create_engine
import config
import pyodbc
import os
from wtforms import SelectField


from wtforms import Form, StringField,TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
# pip install email_validator
# pip install pyodbc
# Register Class
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


conn = pyodbc.connect(config.DATABASE_CONNECTION_STRING)
cursor = conn.cursor()

class RegisterForm(Form):
    user_type = SelectField("User Type", choices=[])
    username = StringField("Username",validators=[validators.Length(min=4, max=25)])
    name = StringField("Name", validators=[validators.Length(min=2, max=25)])
    surname = StringField("Surname", validators=[validators.Length(min=2, max=25)])
    password = PasswordField("Password", validators=[
        validators.DataRequired(message="Enter password.."),
        validators.EqualTo(fieldname = "confirm", message= "password does not match..")
    ])
    confirm = PasswordField("Verify password..")
    email = StringField("Email", validators=[validators.Email(message="invalid email..")])

class LoginForm(Form):
    username = StringField("Username")
    password = PasswordField("Password")








#engine = create_engine(config.DATABASE_URL)

@app.route("/register", methods= ["GET", "POST"])
def register_service():
    form = RegisterForm(request.form)
    
   
    cursor.execute("SELECT Id, UserType FROM UserType")
    user_types = cursor.fetchall()
    
    
    form.user_type.choices = [(str(ut[0]), ut[1]) for ut in user_types]
    
    if request.method == "POST" and form.validate():
        username = form.username.data
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        user_type = form.user_type.data
        hashed_password = sha256_crypt.encrypt(str(form.password.data))
        
        try:
            
            sql = """
            INSERT INTO Users (Username, Name, Surname, Email, Password, UserTypeId)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(sql, (username, name, surname, email, hashed_password, user_type))
            conn.commit()
            flash('You have successfully registered', 'success')
            return redirect(url_for('login_service'))
        except pyodbc.IntegrityError:
            flash('Error: Username or email already exists', 'danger')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
    
    return render_template("register.html", form=form)
    

@app.route("/login", methods= ["GET", "POST"])
def login_service():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data
        user_query = "Select * from users where username= ?"
        cursor.execute(user_query,(username,))
        user_result = cursor.fetchone()
        if user_result:
            real_password =user_result[5]
            if sha256_crypt.verify(password_entered,real_password):
                flash("Login successfull")
                session["logged_in"]=True
                session["username"]= username


                return redirect(url_for("register_service"))
            else:
                flash("invalid password")
                return redirect(url_for("login_service"))
            
        else:
            flash("User is not valid")
            return redirect(url_for("login_service"))
    return render_template("login.html", form=form)

#Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_service"))



if __name__ == '__main__':
    app.run(debug=True, port=5007)


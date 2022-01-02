from flask import Blueprint ,render_template ,redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)

@auth.route("/signup", methods = ['GET', 'POST'])
def signUp():

    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password1")
        confirm_password = request.form.get("password2")


        #extracting email to check wether the email and username already exist in the database
        #if the user is already exists then flash the message to the user that there is an account
        # already in that mail or username 
        email_exists = User.query.filter_by(email = email).first()
        user_name_exists = User.query.filter_by(username = username).first()

        if email_exists:
            flash("Email already in use.", category='error')
        elif user_name_exists:
            flash("username taken.", category='error')
        elif password!=confirm_password:
            flash('Password don\'t match.', category='error')
        elif len(username) < 2:
            flash('Username too short.', category='error')
        elif len(password) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash('Email is invlaid.', category='error')
        else:
            #create a new user
            #sha256 is just an encryption method
            new_user = User(email = email, username = username, password = generate_password_hash(password, method='sha256'))

            #adding new user to database
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User Created', category='success')

            #after adding redirect them to the home page where you can see all your post
            return redirect(url_for('views.home'))

    
    return render_template("signup.html", user = current_user)

@auth.route("/login", methods = ['GET', 'POST'])
def logIn():

    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email = email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('logged in', category= 'success')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist', category='error')


    return render_template("login.html", user = current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
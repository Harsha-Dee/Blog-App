from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"



def createApp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123456789'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
   

    #here since we are pyhton package we use . means from this pyhton package 
    #there is module called views from that module import views
    from .views import views 
    from .auth import auth 

    #registering the routes blueprint
    app.register_blueprint(views, url_prefix = "/")
    app.register_blueprint(auth, url_prefix = "/")

    #before creating the database we must import all our that we need inside our database
    from .models import User, Post, Comment, Like, Reply
    create_database(app)

    #creating login manager
    login_manager = LoginManager()

    #if user tries to access other routes other than login or signup  before creating an account then redirect them to the login page
    login_manager.login_view = "auth.logIn"

    #intilaising login manager
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app = app)
        print("Database created")
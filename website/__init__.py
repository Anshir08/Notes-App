from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()   # database object
DB_NAME = "database.db"  # database name

def create_app():
    app = Flask(__name__)  # creting app with file name

    app.config['SECRET_KEY'] = "qwerty qwerty"  # secret key for cookies and sessions
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"   # connection of database with app 
    db.init_app(app)    # initializing database for the app

    # calling blueprint
    from .views import views
    from .auth import auth

    # register the blueprints with prefix urls
    app.register_blueprint(views, prefix_url='/')
    app.register_blueprint(auth, prefix_url='/')

    from .models import User, Note  # importing classes aka daabase tables

    create_database(app)    # calling function for creating database in the app

    login_manager = LoginManager()      # create an object of login manager
    login_manager.login_view = 'auth.login'  # default page where we are redirected when we are not logged in
    login_manager.init_app(app)     # login in our app

    # load the user using the user_id i.e., the primary key by default
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/'+DB_NAME):     # if database is not already created
        # creating database for the app
        with app.app_context():     
            db.create_all()
        print('Database Created!')
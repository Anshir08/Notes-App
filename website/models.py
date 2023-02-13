from . import db    # it's equivalent to from website import db
from flask_login import UserMixin 
from sqlalchemy.sql import func

# creating Note Class for User's Notes table
class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)  # unique id for every note(primary key)
    data = db.Column(db.String(10000))  # taking notes as string format
    date = db.Column(db.DateTime(timezone=True), default = func.now())  # taking the timestamp for new note

    # one to many relation adding notes to the specific user id used as a foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)  # unique id for every user
    email = db.Column(db.String(150), unique = True)    # unique email id for each user
    password = db.Column(db.String(150))    # user's account password
    first_name = db.Column(db.String(150))  # user's name

    # creating relation of User's table to the specific notes which were 
    # referenced by user id as foreign key in the Notes table
    notes = db.relationship('Note') 

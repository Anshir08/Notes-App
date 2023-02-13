from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)   # creating blueprint

@auth.route('/login', methods = ['POST', 'GET'])   # defining route for the function with methods
def login():
    if request.method == 'POST':    # submitting info
        # retrieving login form data
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()  #checking email data in User database
        # flashing messages after checking the constraints
        if user:
            if check_password_hash(user.password, password):
                login_user(user,remember=True)      # login the user for current session
                flash("Logged In Successfully!", category = 'success')
                return redirect(url_for('views.home'))      
            else:
                flash("Incorrect Password, Try again", category = 'error')
        else:
            flash("Email does not exist.",category = 'error')

    return render_template('/login.html',user = current_user)    # make html interface appear to the client

@auth.route('/logout')   # defining route for the function
@login_required     # only allow access to the function if we logged in
def logout():
    logout_user()   # logout the current user
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods = ['GET','POST'])   # defining route for the function with methods
def sign_up():
    if request.method == 'POST':    # submitting info 
        #   getting form data
        email = request.form.get('email')
        firstname = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()  # checking email data in User database
        # checking constraints
        if user:
            flash("Email already exists.", category = 'error')
        elif len(email) < 4:
            flash('Email must be greater than 3', category='error')
        elif len(firstname) < 2:
            flash('firstname must be greater than 2', category = 'error')
        elif password1 != password2:
            flash('Password don\'t match', category = 'error' )
        elif len(password1) < 7:
            flash('Password must be atleast 7 characters', category = 'error')
        else:
            new_user = User(email = email, first_name = firstname,
                        password = generate_password_hash(password1, method = 'sha256'))   # creating new user with secure password
            db.session.add(new_user)    # adding new user session
            db.session.commit()     # adding session to the database
            login_user(new_user,remember=True)      # login the user for current session
            flash('Account Created', category='success')
            return redirect(url_for('views.home'))  #directing to the home page

    return render_template("signup.html",user = current_user)   # make html interface appear to the client


# Boilerplate grabbed from OnGuard project

from flask import *
from flask_sqlalchemy import *
from flask_login import *
from flask_wtf import *

from __main__ import app, db, User

@app.route('/register/', methods=["GET", "POST"])
def register():
    # If POST request, make new user
    if request.method == "POST":
        # Variable to detect if something went wrong, so multiple flashes can show up
        tripper = False

        # Check if there is username/password
        if len(request.form.get("username")) == 0:
            flash("You need to have a username", 'error')
            tripper = True
        if len(request.form.get("password")) == 0:
            flash("You need to have a password", 'error')
            tripper = True
        
        # Check tripper
        if tripper == True:
            return redirect(url_for("register"))
        
        # Check for existing username
        usernameExists = User.query.filter_by(username=request.form.get("username")).first()
        if usernameExists:
            flash("Username already exists", 'error')
            return redirect(url_for('register'))


        # Check password repeat
        if request.form.get("password") == request.form.get("rpassword"):
            user = User(username=request.form.get("username"), password=request.form.get("password"), role=request.form.get("role"))

            # Implement into db
            db.session.add(user)
            db.session.commit()

            return redirect(url_for("login"))
        else:
            flash("Passwords don't match", 'error')
            return redirect(url_for('register'))

    return render_template('/login/register.html')

# MAYBE: Implement brute force security
@app.route('/login/', methods=["GET", "POST"])
def login():
    # Check for POST request and do login
    if request.method == "POST":
        # No tripper because of structure of flashes

        if len(request.form.get("username")) == 0:
            flash("You need to have a username", 'error')
            return redirect(url_for('login'))

        # Check if username exists before password to avoid looking up
        # Non-existant username in db
        usernameExists = User.query.filter_by(username=request.form.get("username")).first()
        print(usernameExists)
        if usernameExists == None:
            flash("Invalid username/password", 'error')
            return redirect(url_for('login'))

        if len(request.form.get("password")) == 0:
            flash("You need to have a password", 'error')
            return redirect(url_for("login"))


        user = User.query.filter_by(username=request.form.get("username")).first()
        # Check for / validate password
        if user.password == request.form.get("password"):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Invalid username/password", 'error')
            return redirect(url_for('login'))

    return render_template('/login/login.html')
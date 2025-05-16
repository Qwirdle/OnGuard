from flask import Flask, render_template
from flask_login import *
from src.models import db
from src.config import *

app = Flask(__name__)

# Will fix when inconvenience is encountered <3
# login_manager = LoginManager()
# login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def login():
    return render_template('login.html', SCHOOL_NAME = SCHOOL_NAME)

@app.route('/home/')
# @login_required Disabled for UI work
def home():
    return render_template('home.html', SCHOOL_NAME = SCHOOL_NAME)

# Todo: Move to and create error.py routes file
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
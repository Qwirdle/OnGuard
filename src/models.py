from flask_sqlalchemy import *
from flask_login import UserMixin

db = SQLAlchemy() # Initiate sqlalchemy here because models need it first, later imported into app.py

class Users(UserMixin, db.Model):
    """Users database model, main database to handle all the normal user data (specifically login)"""

    id = db.Column(db.Integer, primary_key=True) # Unique identification ID for all user entrys
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)

    fname = db.Column(db.String(250),
                         nullable=False)
    lname = db.Column(db.String(250),
                         nullable=False)
    
    cdate = db.Column(db.String(250),
                         default="none")
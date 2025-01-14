from flask_sqlalchemy import *
from flask_login import UserMixin

db = SQLAlchemy() # Initiate sqlalchemy here because models need it first, later imported into app.py

class Users(UserMixin, db.Model):
    """Users database model, main database to handle all the normal user data (specifically login)
    Additionally, because the relationship is one-to-one, all course progress information is stored here."""

    id = db.Column(db.Integer, primary_key=True)  # Unique identification ID for all user entries
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    fname = db.Column(db.String(250), nullable=False)
    lname = db.Column(db.String(250), nullable=False)

    cdate = db.Column(db.String(250), default="none")

    # Article progress columns for all chapters
    #   0 is unstarted, 1 is in progress, and 2 is completed
    # Chapter 1
    article_1_1 = db.Column(db.Integer, default=2)
    article_1_2 = db.Column(db.Integer, default=1)
    article_1_3 = db.Column(db.Integer, default=1)

    # Chapter 2
    article_2_1 = db.Column(db.Integer, default=2)
    article_2_2 = db.Column(db.Integer, default=2)
    article_2_3 = db.Column(db.Integer, default=2)
    article_2_4 = db.Column(db.Integer, default=2)

    # Chapter 3
    article_3_1 = db.Column(db.Integer, default=1)
    article_3_2 = db.Column(db.Integer, default=1)
    article_3_3 = db.Column(db.Integer, default=1)
    article_3_4 = db.Column(db.Integer, default=1)

    # Chapter 4
    article_4_1 = db.Column(db.Integer, default=0)
    article_4_2 = db.Column(db.Integer, default=2)
    article_4_3 = db.Column(db.Integer, default=0)
    article_4_4 = db.Column(db.Integer, default=0)

    # Chapter 5
    article_5_1 = db.Column(db.Integer, default=0)
    article_5_2 = db.Column(db.Integer, default=0)
    article_5_3 = db.Column(db.Integer, default=0)
    article_5_4 = db.Column(db.Integer, default=0)

    # Chapter 6
    article_6_1 = db.Column(db.Integer, default=0)
    article_6_2 = db.Column(db.Integer, default=0)
    article_6_3 = db.Column(db.Integer, default=0)
    article_6_4 = db.Column(db.Integer, default=0)

    # Chapter 7
    article_7_1 = db.Column(db.Integer, default=0)
    article_7_2 = db.Column(db.Integer, default=0)
    article_7_3 = db.Column(db.Integer, default=0)

    # Chapter 8
    article_8_1 = db.Column(db.Integer, default=0)
    article_8_2 = db.Column(db.Integer, default=0)
    article_8_3 = db.Column(db.Integer, default=0)

    # Chapter 9
    article_9_1 = db.Column(db.Integer, default=0)
    article_9_2 = db.Column(db.Integer, default=0)
    article_9_3 = db.Column(db.Integer, default=0)

    # Chapter 10
    article_10_1 = db.Column(db.Integer, default=0)
    article_10_2 = db.Column(db.Integer, default=0)
    article_10_3 = db.Column(db.Integer, default=0)

    # Chapter 11
    article_11_1 = db.Column(db.Integer, default=0)
    article_11_2 = db.Column(db.Integer, default=0)
    article_11_3 = db.Column(db.Integer, default=0)

    # Chapter 12
    article_12_1 = db.Column(db.Integer, default=0)
    article_12_2 = db.Column(db.Integer, default=0)
    article_12_3 = db.Column(db.Integer, default=0)
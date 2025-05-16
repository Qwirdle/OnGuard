from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class File(db.Model):
    __tablename__ = 'files'
    file_id = db.Column(db.Integer, primary_key=True)
    filepath = db.Column(db.String)

    # Relationships
    users = db.relationship('User', backref='file', lazy=True)
    classes = db.relationship('Class', backref='file', lazy=True)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    enrolled_classes = db.relationship(
        'Class',
        secondary='class_enrollment',
        back_populates='students'
    )

    teaching_classes = db.relationship(
        'Class',
        secondary='class_faculty',
        back_populates='faculty'
    )

    grades = db.relationship('Gradebook', backref='user', lazy=True)


class Class(db.Model):
    __tablename__ = 'classes'
    class_id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer)  # foreign-like ref via association table
    file_id = db.Column(db.Integer, db.ForeignKey('files.file_id'))
    name = db.Column(db.String)

    # Relationships
    assignments = db.relationship('Assignment', backref='class_', lazy=True)

    students = db.relationship(
        'User',
        secondary='class_enrollment',
        back_populates='enrolled_classes'
    )

    faculty = db.relationship(
        'User',
        secondary='class_faculty',
        back_populates='teaching_classes'
    )


class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'))
    assignment_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    role = db.Column(db.String)

    # Relationships
    grades = db.relationship('Gradebook', backref='assignment', lazy=True)


class Gradebook(db.Model):
    __tablename__ = 'gradebook'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.assignment_id'), primary_key=True)
    grade = db.Column(db.Integer)


class_enrollment = db.Table(
    'class_enrollment',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('classes.class_id'), primary_key=True)
)

class_faculty = db.Table(
    'class_faculty',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('faculty_id', db.Integer, primary_key=True)  # Not a real FK, just as per DBML
)

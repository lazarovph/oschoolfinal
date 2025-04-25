from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='student')  # 'student', 'teacher', 'admin'
    level = db.Column(db.String(10))  # A1, A2, B1 и т.н.
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    submissions = db.relationship('Submission', backref='student', lazy=True)

# Примерен модел за отчети
from app import db
from datetime import datetime

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

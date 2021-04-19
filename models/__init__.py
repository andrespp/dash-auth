"""models.py
"""
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """User table definition
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    modified = db.Column(db.DateTime)
    active = db.Column(db.Boolean, nullable=False)

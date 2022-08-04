from email.policy import default
from time import time
from pytz import timezone
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from os import path

db_detail = { 'db' : SQLAlchemy(), 'DB_NAME' : 'database.db' } # this is cargo ( easy export )
db = db_detail['db']
DB_NAME = db_detail['DB_NAME']

class user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(40), nullable=False)
    second_name = db.Column(db.String(40), nullable=False)
    notes = db.relationship('notes')

class notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000), nullable=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

def create_database(app):
    if ( not path.exists('website/' + DB_NAME) ): # check path exist or rather a File  
        db.create_all(app=app)
        print('Database created')
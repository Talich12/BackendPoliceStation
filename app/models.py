from app import db, ma
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow_sqlalchemy import fields, auto_field
from marshmallow import Schema, fields
from hashlib import md5
import base64
from datetime import datetime, timedelta
import os
  

class AutoPark(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    mark = db.Column(db.String(), nullable=False)
    model = db.Column(db.String(), nullable=False)

class Armory(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    weapon_type = db.Column(db.String(), nullable=False)
    code = db.Column(db.String(), nullable=False)
    full_name = db.Column(db.String(), nullable=False)

    policeman_id = db.Column(db.Integer, db.ForeignKey('policeman.id'), nullable=True)
    policeman = db.relationship("Policeman", backref="weapon")

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)

class Policeman(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    sername = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    job = db.relationship("Job", backref="policeman")
    hire_date = db.Column(db.DateTime(), nullable=False) #ДАТА
    birthday = db.Column(db.DateTime(), nullable=False) #ДАТА

class Trainee(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    sername = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    birthday = db.Column(db.DateTime(), nullable=False) # ДАТА
    curator_id = db.Column(db.Integer, db.ForeignKey('policeman.id'), nullable=False)
    curator = db.relationship("Policeman", backref="trainee")

class CarAccounting(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('auto_park.id'), nullable=False)
    car = db.relationship("AutoPark", backref="account")
    policeman_id = db.Column(db.Integer, db.ForeignKey('policeman.id'), nullable=False)
    policeman = db.relationship("Policeman", backref="trainee")


class Criminal(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    sername = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    birthday = db.Column(db.DateTime(), nullable=False) #ДАТА
    status = db.Column(db.String(), nullable=False)

class Detention(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    criminal_id = db.Column(db.Integer, db.ForeignKey('criminal.id'), nullable=False)
    car = db.relationship("Criminal", backref="detention")
    policeman_id = db.Column(db.Integer, db.ForeignKey('policeman.id'), nullable=False)
    policeman = db.relationship("Policeman", backref="detention")
    article = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime,  nullable=False) #ДАТА

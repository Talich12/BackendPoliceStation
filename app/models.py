from app import db, ma
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow_sqlalchemy import fields, auto_field
from marshmallow import Schema, fields
from hashlib import md5
import base64
from datetime import datetime, timedelta
import os

class Appeal(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    sername = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    adress = db.Column(db.String(), nullable=False)
    birthday = db.Column(db.Date(), nullable=False) # ДАТА
    report = db.Column(db.String(), nullable=False)
    date = db.Column(db.Date(), nullable=False) #ДАТА

class AutoPark(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    mark = db.Column(db.String(), nullable=False)
    model = db.Column(db.String(), nullable=False)

class Armory(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    weapon_type = db.Column(db.String(), nullable=False)
    code = db.Column(db.String(), nullable=False)
    full_name = db.Column(db.String(), nullable=False)

class ArmoryAccounting(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    policeman_id = db.Column(db.Integer, db.ForeignKey('policeman.id', ondelete='CASCADE'), nullable=True)
    policeman = db.relationship("Policeman", backref="armory_accounting")
    weapon_id = db.Column(db.Integer, db.ForeignKey('armory.id', ondelete='CASCADE'), nullable=True)
    weapon = db.relationship("Armory", backref="armory_accounting")

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.String(), nullable=False)

class Policeman(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    sername = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='SET NULL'), nullable=True)
    job = db.relationship("Job", backref="policeman")
    hire_date = db.Column(db.Date(), nullable=False) #ДАТА
    birthday = db.Column(db.Date(), nullable=False) #ДАТА

class Trainee(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    sername = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    birthday = db.Column(db.Date(), nullable=False) # ДАТА
    curator_id = db.Column(db.Integer, db.ForeignKey('policeman.id', ondelete='SET NULL'), nullable=True)
    curator = db.relationship("Policeman", backref="trainee")

class CarAccounting(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('auto_park.id',  ondelete='CASCADE'), nullable=True)
    car = db.relationship("AutoPark", backref="account")
    policeman_id = db.Column(db.Integer, db.ForeignKey('policeman.id', ondelete='CASCADE'), nullable=True)
    policeman = db.relationship("Policeman", backref="account")


class Criminal(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    sername = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    birthday = db.Column(db.Date(), nullable=False) #ДАТА
    status_id = db.Column(db.Integer, db.ForeignKey('status.id', ondelete='SET NULL'), nullable=True)
    status = db.relationship("Status", backref="criminal")

class Detention(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    criminal_id = db.Column(db.Integer, db.ForeignKey('criminal.id'), nullable=False)
    criminal = db.relationship("Criminal", backref="detention")
    policeman_id = db.Column(db.Integer, db.ForeignKey('policeman.id', ondelete='SET NULL'), nullable=True)
    policeman = db.relationship("Policeman", backref="detention")
    article = db.Column(db.String(), nullable=False)
    report = db.Column(db.String(), nullable=False)
    date = db.Column(db.Date,  nullable=False) #ДАТА

class AutoParkSchema(ma.SQLAlchemySchema):
    class Meta:
        model = AutoPark
        load_instance = True

    id =auto_field()
    mark = auto_field()
    model = auto_field()

class JobSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Job
        load_instance = True

    id =auto_field()
    name = auto_field()

class StatusSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Status
        load_instance = True

    id =auto_field()
    status = auto_field()

class AllPolicemanSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Policeman
        load_instance = True

    id = auto_field()
    name = auto_field()
    sername = auto_field()
    lastname = auto_field()
    job_name = fields.Method("get_job_name")
    hire_date = auto_field()
    birthday = auto_field()

    inicials = fields.Method("get_policeman_fullname")

    def get_job_name(self, obj):
        return obj.job.name if obj.job else ''
    
    def get_policeman_fullname(self, obj):
        lastname = str(obj.lastname)
        name = str(obj.name)
        sername = str(obj.sername)

        output = f"{lastname} {name[0]}. {sername[0]}."
        return output


class PolicemanSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Policeman
        load_instance = True

    id = auto_field()
    name = auto_field()
    sername = auto_field()
    lastname = auto_field()
    job = fields.Nested(JobSchema)
    job_id = auto_field()
    hire_date = auto_field()
    birthday = auto_field()

class CarAccountingSchema(ma.SQLAlchemySchema):
    class Meta:
        model = CarAccounting
        load_instance = True

    id = auto_field()
    car = fields.Nested(AutoParkSchema)
    policeman = fields.Nested(AllPolicemanSchema)


class AllArmorySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Armory
        load_instance = True

    id = auto_field()
    weapon_type = auto_field()
    code = auto_field()
    full_name = auto_field()

    status = fields.Method("get_status")

    def get_status(self, obj):
        find = ArmoryAccounting.query.filter_by(weapon_id = obj.id).first()

        if find is None:
            return "На складе"
        else:
            return "На руках"
    
class ArmorySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Armory
        load_instance = True

    id = auto_field()
    weapon_type = auto_field()
    code = auto_field()
    full_name = auto_field()
    status = fields.Method("get_status")

    def get_status(self, obj):
        find = ArmoryAccounting.query.filter_by(weapon_id = obj.id).first()

        if find is None:
            return "На складе"
        else:
            return "На руках"

class AllTraineeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Trainee
        load_instance = True

    id = auto_field()
    name = auto_field()
    sername = auto_field()
    lastname = auto_field()
    birthday = auto_field()

    curator_fullname = fields.Method('get_curator_fullname')

    
    def get_curator_fullname(self, obj):
        if obj.curator:
            lastname = str(obj.curator.lastname)
            name = str(obj.curator.name)
            sername = str(obj.curator.sername)

            output = f"{lastname} {name[0]}. {sername[0]}."

        else:
            output = ""
        return output

class TraineeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Trainee
        load_instance = True

    id = auto_field()
    name = auto_field()
    sername = auto_field()
    lastname = auto_field()
    birthday = auto_field()
    curator_id = auto_field()

    curator = fields.Nested(AllPolicemanSchema)

class CriminalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Criminal
        load_instance = True

    id = auto_field()
    name = auto_field()
    sername = auto_field()
    lastname = auto_field()
    birthday = auto_field()
    status = fields.Nested(StatusSchema)
    status_id = auto_field()

    inicials = fields.Method('get_inicials')

    def get_inicials(self, obj):
        lastname = str(obj.lastname)
        name = str(obj.name)
        sername = str(obj.sername)

        output = f"{lastname} {name[0]}. {sername[0]}."
        return output

class AllDetentionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Detention
        load_instance = True

    id = auto_field()
    criminal_fullname = fields.Method("get_criminal_fullname")
    policeman_fullname = fields.Method("get_policeman_fullname")
    article = auto_field()
    report = auto_field()
    date = auto_field()

    def get_policeman_fullname(self, obj):
        if obj.policeman:
            lastname = str(obj.policeman.lastname)
            name = str(obj.policeman.name)
            sername = str(obj.policeman.sername)

            output = f"{lastname} {name[0]}. {sername[0]}."

        else:
            output = ""
        return output
    
    def get_criminal_fullname(self, obj):
        if obj.criminal:
            lastname = str(obj.criminal.lastname)
            name = str(obj.criminal.name)
            sername = str(obj.criminal.sername)

            output = f"{lastname} {name[0]}. {sername[0]}."

        else:
            output = ""
        return output

class DetentionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Detention
        load_instance = True

    id = auto_field()
    criminal = fields.Nested(CriminalSchema)
    policeman = fields.Nested(AllPolicemanSchema)
    article = auto_field()
    date = auto_field()
    report = auto_field()

class ArmoryAccrountingSchema(ma.SQLAlchemySchema):
    class Meta:
        model = CarAccounting
        load_instance = True

    id = auto_field()
    policeman = fields.Nested(AllPolicemanSchema)
    weapon = fields.Nested(AllArmorySchema)

class AppealSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Appeal
        load_instance = True

    id = auto_field()
    name = auto_field()
    sername = auto_field()
    lastname = auto_field()
    adress = auto_field()
    birthday = auto_field()
    report = auto_field()
    date = auto_field()
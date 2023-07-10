from app import app, db
from flask import jsonify, request
from app.models import Policeman, PolicemanSchema, AllPolicemanSchema, Armory, ArmorySchema, CarAccounting, CarAccountingSchema, Detention, Trainee
from datetime import datetime

@app.route('/policeman', methods = ['GET'])
def get_policeman():
    policeman_schema = AllPolicemanSchema(many = True)

    req = Policeman.query.all()

    output = policeman_schema.dump(req)
    return jsonify(output)

@app.route('/policeman/gun', methods = ['GET'])
def get_policeman_gun():
    policeman_schema = PolicemanSchema(many = True)

    subquery = db.session.query(Armory.policeman_id).distinct()

    req = db.session.query(Policeman).filter(Policeman.id.in_(subquery)).all()


    output = policeman_schema.dump(req)
    return jsonify(output)

@app.route('/policeman/gun/not', methods = ['GET'])
def get_policeman_gun_not():
    policeman_schema = PolicemanSchema(many = True)

    subquery = db.session.query(Armory.policeman_id).distinct()

    req = Policeman.query.filter(~Policeman.id.in_(subquery)).all()


    output = policeman_schema.dump(req)
    return jsonify(output)


@app.route('/policeman', methods = ['POST'])
def post_policeman():
    data = request.get_json()
    name = data['name']
    sername = data['sername']
    lastname = data['lastname']
    job_id = data['job_id']
    hire_date = data['hire_date']
    birthday = data['birthday']

    hire_date = datetime.strptime(hire_date, '%Y-%m-%d').date()
    birthday = datetime.strptime(birthday, '%Y-%m-%d').date()

    policeman = Policeman(name = name, sername = sername, lastname = lastname, job_id = job_id,
                          hire_date = hire_date, birthday = birthday)
    
    db.session.add(policeman)
    db.session.commit()

    return {"message": "Success"}

@app.route('/policeman/<id>', methods = ['GET'])
def get_cur_policeman(id):
    policeman_schema = PolicemanSchema(many = False)

    req = Policeman.query.filter_by(id = id).first()

    output = policeman_schema.dump(req)
    return jsonify(output)

@app.route('/policeman/<id>/gun', methods = ['GET'])
def get_cur_policeman_gun(id):
    armory_schema = ArmorySchema(many = True)

    req = Armory.query.filter_by(policeman_id = id).all()

    output = armory_schema.dump(req)

    output = armory_schema.dump(req)
    return jsonify(output)

@app.route('/policeman/<id>/auto', methods = ['GET'])
def get_cur_policeman_auto(id):
    output = []
    auto_schema = CarAccountingSchema(many = True)

    req = CarAccounting.query.filter_by(policeman_id = id).all()

    req = auto_schema.dump(req)
    for item in req:
        output.append(item['car'])

    return jsonify(output)

@app.route('/policeman/<id>', methods = ['POST'])
def edit_cur_policeman(id):
    data = request.get_json()
    name = data['name']
    sername = data['sername']
    lastname = data['lastname']
    job_id = data['job_id']
    hire_date = data['hire_date']
    birthday = data['birthday']

    hire_date = datetime.strptime(hire_date, '%Y-%m-%d').date()
    birthday = datetime.strptime(birthday, '%Y-%m-%d').date()

    policeman = Policeman.query.filter_by(id = id).first()
    policeman.name = name
    policeman.sername = sername
    policeman.lastname = lastname
    policeman.job_id = job_id
    policeman.hire_date = hire_date
    policeman.birthday = birthday
    db.session.commit()

    return {"message": "Success"}

@app.route('/policeman/<id>', methods = ['DELETE'])
def delete_cur_policeman(id):
    policeman = Policeman.query.filter_by(id = id).first()

    find_cars = CarAccounting.query.filter_by(policeman_id = id).all()
    for car in find_cars:
        db.session.delete(car)

    db.session.delete(policeman)
    db.session.commit()
    
    return {"message": "Success"}

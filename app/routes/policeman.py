from app import app, db
from flask import jsonify, request
from app.models import Policeman, PolicemanSchema
from datetime import datetime

@app.route('/policeman', methods = ['GET'])
def get_policeman():
    policeman_schema = PolicemanSchema(many = True)

    req = Policeman.query.all()

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

    db.session.delete(policeman)
    db.session.commit()
    
    return {"message": "Success"}

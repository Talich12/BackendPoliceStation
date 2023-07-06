from app import app, db
from flask import jsonify, request
from app.models import Trainee, TraineeSchema
from datetime import datetime

@app.route('/trainee', methods = ['GET'])
def get_trainee():
    trainee_schema = TraineeSchema(many = True)

    req = Trainee.query.all()

    output = trainee_schema.dump(req)
    return jsonify(output)

@app.route('/trainee', methods = ['POST'])
def post_trainee():
    data = request.get_json()
    name = data['name']
    sername = data['sername']
    lastname = data['lastname']
    birthday = data['birthday']
    curator_id = data['curator_id']

    birthday = datetime.strptime(birthday, '%Y-%m-%d').date()

    trainee = Trainee(name = name, sername = sername, lastname = lastname, birthday = birthday, curator_id = curator_id)
    db.session.add(trainee)
    db.session.commit()

    return {"message": "Success"}

@app.route('/trainee/<id>', methods = ['GET'])
def get_cur_trainee(id):
    trainee_schema = TraineeSchema(many = False)

    req = Trainee.query.filter_by(id = id).first()

    output = trainee_schema.dump(req)
    return jsonify(output)


@app.route('/trainee/<id>', methods = ['POST'])
def edit_cur_trainee(id):
    data = request.get_json()
    name = data['name']
    sername = data['sername']
    lastname = data['lastname']
    birthday = data['birthday']
    curator_id = data['curator_id']

    birthday = datetime.strptime(birthday, '%Y-%m-%d').date()

    traynee = Trainee.query.filter_by(id = id).first()
    traynee.name = name
    traynee.sername = sername
    traynee.lastname = lastname
    traynee.birthday = birthday
    traynee.curator_id = curator_id
    db.session.commit()

    return {"message": "Success"}

@app.route('/trainee/<id>', methods = ['DELETE'])
def delete_cur_trainee(id):
    traynee = Trainee.query.filter_by(id = id).first()

    db.session.delete(traynee)
    db.session.commit()
    
    return {"message": "Success"}

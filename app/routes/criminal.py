from app import app, db
from flask import jsonify, request
from app.models import Criminal, CriminalSchema, Status
from datetime import datetime

@app.route('/criminal', methods = ['GET'])
def get_criminal():
    criminal_schema = CriminalSchema(many = True)

    req = Criminal.query.all()

    output = criminal_schema.dump(req)
    return jsonify(output)

@app.route('/criminal/free', methods = ['GET'])
def get_criminal_free():
    criminal_schema = CriminalSchema(many = True)

    req = Criminal.query.join(Status).filter(Status.status == "Свободен").all()

    output = criminal_schema.dump(req)
    return jsonify(output)

@app.route('/criminal/free/not', methods = ['GET'])
def get_criminal_free_not():
    criminal_schema = CriminalSchema(many = True)

    req = Criminal.query.join(Status).filter(Status.status != "Свободен").all()

    output = criminal_schema.dump(req)
    return jsonify(output)

@app.route('/criminal', methods = ['POST'])
def post_criminal():
    data = request.get_json()
    name = data['name']
    sername = data['sername']
    lastname = data['lastname']
    birthday = data['birthday']
    status_id = data['status_id']

    birthday = datetime.strptime(birthday, '%Y-%m-%d').date()

    criminal = Criminal(name = name, sername = sername, lastname = lastname, birthday = birthday, status_id = status_id)
    db.session.add(criminal)
    db.session.commit()

    return {"message": "Success"}

@app.route('/criminal/<id>', methods = ['GET'])
def get_cur_criminal(id):
    criminal_schema = CriminalSchema(many = False)

    req = Criminal.query.filter_by(id = id).first()

    output = criminal_schema.dump(req)
    return jsonify(output)


@app.route('/criminal/<id>', methods = ['POST'])
def edit_cur_criminal(id):
    data = request.get_json()
    name = data['name']
    sername = data['sername']
    lastname = data['lastname']
    birthday = data['birthday']
    status_id = data['status_id']

    birthday = datetime.strptime(birthday, '%Y-%m-%d').date()

    criminal = Criminal.query.filter_by(id = id).first()
    criminal.name = name
    criminal.sername = sername
    criminal.lastname = lastname
    criminal.birthday = birthday
    criminal.status_id = status_id
    db.session.commit()

    return {"message": "Success"}

@app.route('/criminal/<id>', methods = ['DELETE'])
def delete_cur_criminal(id):
    criminal = Criminal.query.filter_by(id = id).first()

    db.session.delete(criminal)
    db.session.commit()
    
    return {"message": "Success"}

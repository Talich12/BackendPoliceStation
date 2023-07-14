from app import app, db
from flask import jsonify, request
from app.models import Appeal, AppealSchema
from datetime import datetime

@app.route('/appeal', methods = ['GET'])
def get_appeal():
    job_schema = AppealSchema(many = True)

    req = Appeal.query.all()

    output = job_schema.dump(req)
    return jsonify(output)

@app.route('/appeal', methods = ['POST'])
def post_appeal():
    data = request.get_json()
    name = data['name']
    sername =data['sername']
    lastname = data['lastname']
    adress = data['adress']
    birthday = data['birthday']
    date = data['date']
    report = data['report']

    date = datetime.strptime(date, '%Y-%m-%d').date()
    birthday = datetime.strptime(birthday, '%Y-%m-%d').date()

    job = Appeal(name = name, sername = sername, lastname = lastname, adress = adress, birthday = birthday, date = date, report = report)
    db.session.add(job)
    db.session.commit()

    return {"message": "Success"}

@app.route('/appeal/<id>', methods = ['GET'])
def get_cur_appeal(id):
    job_schema = AppealSchema(many = False)

    req = Appeal.query.filter_by(id = id).first()

    output = job_schema.dump(req)
    return jsonify(output)


@app.route('/appeal/<id>', methods = ['POST'])
def edit_cur_appeal(id):
    data = request.get_json()
    name = data['name']
    sername =data['sername']
    lastname = data['lastname']
    adress = data['adress']
    birthday = data['birthday']
    date = data['date']
    report = data['report']

    date = datetime.strptime(date, '%Y-%m-%d').date()
    birthday = datetime.strptime(birthday, '%Y-%m-%d').date()

    job = Appeal.query.filter_by(id = id).first()
    job.name = name
    job.sername = sername
    job.lastname = lastname
    job.adress = adress
    job.birthday = birthday
    job.date = date
    job.report = report
    db.session.commit()

    return {"message": "Success"}

@app.route('/appeal/<id>', methods = ['DELETE'])
def delete_cur_appeal(id):
    job = Appeal.query.filter_by(id = id).first()

    db.session.delete(job)
    db.session.commit()
    
    return {"message": "Success"}
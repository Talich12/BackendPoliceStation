from app import app, db
from flask import jsonify, request
from app.models import Detention, DetentionSchema
from datetime import datetime

@app.route('/detention', methods = ['GET'])
def get_detention():
    detention_schema = DetentionSchema(many = True)

    req = Detention.query.all()

    output = detention_schema.dump(req)
    return jsonify(output)

@app.route('/detention', methods = ['POST'])
def post_detention():
    data = request.get_json()
    policeman_id = data['policeman_id']
    criminal_id = data['criminal_id']
    article = data['article']
    date = data['date']

    date = datetime.strptime(date, '%Y-%m-%d').date()

    detention = Detention(policeman_id = policeman_id, criminal_id = criminal_id, article = article, date = date)
    db.session.add(detention)
    db.session.commit()

    return {"message": "Success"}

@app.route('/detention/<id>', methods = ['GET'])
def get_cur_detention(id):
    detention_schema = DetentionSchema(many = False)

    req = Detention.query.filter_by(id = id).first()

    output = detention_schema.dump(req)
    return jsonify(output)


@app.route('/detention/<id>', methods = ['POST'])
def edit_cur_detention(id):
    data = request.get_json()
    policeman_id = data['policeman_id']
    criminal_id = data['criminal_id']
    article = data['article']
    date = data['date']

    date = datetime.strptime(date, '%Y-%m-%d').date()

    detention = Detention.query.filter_by(id = id).first()
    detention.policeman_id = policeman_id
    detention.criminal_id = criminal_id
    detention.article = article
    detention.date = date
    db.session.commit()

    return {"message": "Success"}

@app.route('/detention/<id>', methods = ['DELETE'])
def delete_cur_detention(id):
    detention = Detention.query.filter_by(id = id).first()

    db.session.delete(detention)
    db.session.commit()
    
    return {"message": "Success"}

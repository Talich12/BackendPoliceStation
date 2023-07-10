from app import app, db
from flask import jsonify, request
from app.models import Status, StatusSchema
from datetime import datetime


@app.route('/status', methods = ['GET'])
def get_status():
    status_schema = StatusSchema(many = True)

    req = Status.query.all()

    output = status_schema.dump(req)
    return jsonify(output)

@app.route('/status', methods = ['POST'])
def post_status():
    data = request.get_json()
    status = data['status']

    status = Status(status = status)

    db.session.add(status)
    db.session.commit()

    return {"message": "Success"}

@app.route('/status/<id>', methods = ['Delete'])
def delete_status(id):
    

    status = Status.query.filter_by(id = id).first()

    db.session.delete(status)
    db.session.commit()

    return {"message": "Success"}
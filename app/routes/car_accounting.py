from app import app, db
from flask import jsonify, request
from app.models import CarAccounting, CarAccountingSchema
from datetime import datetime

@app.route('/car-account', methods = ['GET'])
def get_car_account():
    car_account_schema = CarAccountingSchema(many = True)

    req = CarAccounting.query.all()

    output = car_account_schema.dump(req)
    return jsonify(output)

@app.route('/car-account', methods = ['POST'])
def post_car_account():
    data = request.get_json()
    car_id = data['car_id']
    policeman_id = data['policeman_id']

    car_account = CarAccounting(car_id = car_id, policeman_id = policeman_id)
    
    db.session.add(car_account)
    db.session.commit()

    return {"message": "Success"}

@app.route('/car-account/<id>', methods = ['GET'])
def get_cur_car_account(id):
    car_account_schema = CarAccountingSchema(many = False)

    req = CarAccounting.query.filter_by(id = id).first()

    output = car_account_schema.dump(req)
    return jsonify(output)


@app.route('/car-account/<id>', methods = ['POST'])
def edit_cur_car_account(id):
    data = request.get_json()
    car_id = data['car_id']
    policeman_id = data['policeman_id']

    car_account = CarAccounting.query.filter_by(id = id).first()
    car_account.car_id = car_id
    car_account.policeman_id = policeman_id

    db.session.commit()

    return {"message": "Success"}

@app.route('/car-account/<id>', methods = ['DELETE'])
def delete_cur_car_account(id):
    car_account = CarAccounting.query.filter_by(id = id).first()

    db.session.delete(car_account)
    db.session.commit()
    
    return {"message": "Success"}

@app.route('/car-account/<id>/policeman', methods = ['DELETE'])
def delete_cur_car_account_by_policeman_id(id):
    car_account = CarAccounting.query.filter_by(policeman_id = id).first()

    db.session.delete(car_account)
    db.session.commit()
    
    return {"message": "Success"}

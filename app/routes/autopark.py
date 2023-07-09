from app import app, db
from flask import jsonify, request
from app.models import AutoPark, AutoParkSchema, CarAccounting, CarAccountingSchema, Policeman, AllPolicemanSchema

@app.route('/autopark', methods = ['GET'])
def get_autopark():
    autopark_schema = AutoParkSchema(many = True)

    req = AutoPark.query.all()

    output = autopark_schema.dump(req)
    return jsonify(output)

@app.route('/autopark', methods = ['POST'])
def post_autopark():
    data = request.get_json()
    mark = data['mark']
    model = data['model']

    car = AutoPark(mark = mark, model = model)
    db.session.add(car)
    db.session.commit()

    return {"message": "Success"}

@app.route('/autopark/<id>', methods = ['GET'])
def get_cur_car(id):
    autopark_schema = AutoParkSchema(many = False)

    req = AutoPark.query.filter_by(id = id).first()

    output = autopark_schema.dump(req)
    return jsonify(output)


@app.route('/autopark/<id>/policeman', methods = ['GET'])
def get_cur_car_policeman(id):
    output = []
    auto_schema = CarAccountingSchema(many = True)

    req = CarAccounting.query.filter_by(car_id = id).all()

    req = auto_schema.dump(req)
    for item in req:
        output.append(item['policeman'])

    return jsonify(output)

@app.route('/autopark/<id>/policeman/not', methods = ['GET'])
def get_cur_car_policeman_not(id):
    output = []
    policeman_schema = AllPolicemanSchema(many = True)

    subquery = db.session.query(CarAccounting.policeman_id).filter(CarAccounting.car_id == id)

    req2 = Policeman.query.filter(~Policeman.id.in_(subquery)).all()

    output = policeman_schema.dump(req2)

    return jsonify(output)

@app.route('/autopark/<id>', methods = ['POST'])
def edit_cur_car(id):
    data = request.get_json()
    mark = data['mark']
    model = data['model']


    car = AutoPark.query.filter_by(id = id).first()
    car.mark = mark
    car.model = model
    db.session.commit()

    return {"message": "Success"}

@app.route('/autopark/<id>', methods = ['DELETE'])
def delete_cur_car(id):
    car = AutoPark.query.filter_by(id = id).first()

    find_cars = CarAccounting.query.filter_by(car_id = id).all()
    for car in find_cars:
        db.session.delete(car)

    db.session.delete(car)
    db.session.commit()
    
    return {"message": "Success"}

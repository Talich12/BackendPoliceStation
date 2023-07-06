from app import app, db
from flask import jsonify, request
from app.models import AutoPark, AutoParkSchema

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


@app.route('/autopark/<id>', methods = ['POST'])
def edit_cur_car(id):
    data = request.get_json()
    mark = data['mark']
    model = data['model']

    autopark_schema = AutoParkSchema(many = False)

    car = AutoPark.query.filter_by(id = id).first()
    car.mark = mark
    car.model = model
    db.session.commit()

    return {"message": "Success"}

@app.route('/autopark/<id>', methods = ['DELETE'])
def delete_cur_car(id):
    car = AutoPark.query.filter_by(id = id).first()

    db.session.delete(car)
    db.session.commit()
    
    return {"message": "Success"}

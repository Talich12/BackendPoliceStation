from app import app, db
from flask import jsonify, request
from app.models import Armory, ArmorySchema

@app.route('/armory', methods = ['GET'])
def get_armory():
    armory_schema = ArmorySchema(many = True)

    req = Armory.query.all()

    output = armory_schema.dump(req)
    return jsonify(output)

@app.route('/armory', methods = ['POST'])
def post_armory():
    data = request.get_json()
    weapon_type = data['weapon_type']
    code = data['code']
    full_name = data['full_name']
    policeman_id = data['policeman_id']

    armory = Armory(weapon_type = weapon_type, code = code, full_name = full_name, policeman_id = policeman_id)
    db.session.add(armory)
    db.session.commit()

    return {"message": "Success"}

@app.route('/armory/<id>', methods = ['GET'])
def get_cur_armory(id):
    armory_schema = ArmorySchema(many = False)

    req = Armory.query.filter_by(id = id).first()

    output = armory_schema.dump(req)
    return jsonify(output)


@app.route('/armory/<id>', methods = ['POST'])
def edit_cur_armory(id):
    data = request.get_json()
    weapon_type = data['weapon_type']
    code = data['code']
    full_name = data['full_name']
    policeman_id = data['policeman_id']

    armory = Armory.query.filter_by(id = id).first()
    armory.weapon_type = weapon_type
    armory.code = code
    armory.full_name = full_name
    armory.policeman_id = policeman_id
    db.session.commit()

    return {"message": "Success"}

@app.route('/armory/<id>', methods = ['DELETE'])
def delete_cur_armory(id):
    armory = Armory.query.filter_by(id = id).first()

    db.session.delete(armory)
    db.session.commit()
    
    return {"message": "Success"}

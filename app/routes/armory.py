from app import app, db
from flask import jsonify, request
from app.models import Armory, ArmorySchema, AllArmorySchema

@app.route('/armory', methods = ['GET'])
def get_armory():
    armory_schema = AllArmorySchema(many = True)

    req = Armory.query.all()

    output = armory_schema.dump(req)
    return jsonify(output)

@app.route('/armory/not', methods = ['GET'])
def get_armory_not():
    armory_schema = AllArmorySchema(many = True)

    req = Armory.query.all()

    output = armory_schema.dump(req)
    ids = []
    for weapon in output:
        print(weapon['status'])
        if weapon['status'] == "На руках":
            ids.append(weapon)

    for id in ids:
        output.remove(id)
    return jsonify(output)

@app.route('/armory', methods = ['POST'])
def post_armory():
    data = request.get_json()
    weapon_type = data['weapon_type']
    code = data['code']
    full_name = data['full_name']

    armory = Armory(weapon_type = weapon_type, code = code, full_name = full_name)
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

    armory = Armory.query.filter_by(id = id).first()
    armory.weapon_type = weapon_type
    armory.code = code
    armory.full_name = full_name
    db.session.commit()

    return {"message": "Success"}

@app.route('/armory/<id>', methods = ['DELETE'])
def delete_cur_armory(id):
    armory = Armory.query.filter_by(id = id).first()

    db.session.delete(armory)
    db.session.commit()
    
    return {"message": "Success"}

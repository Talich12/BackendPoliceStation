from app import app, db
from flask import jsonify, request
from app.models import ArmoryAccounting

@app.route('/armory-account', methods = ['POST'])
def post_armory_account():
    data = request.get_json()
    policeman_id = data['policeman_id']
    armory_id = data['armory_id']

    find = ArmoryAccounting.query.filter_by(weapon_id = armory_id).first()

    if find is None:
        armory = ArmoryAccounting(policeman_id = policeman_id, weapon_id = armory_id)
        db.session.add(armory)
        db.session.commit()
        return {"message": "Success"}
    else:
        return {"message": "Denied"}
    
@app.route('/armory-account/<id>', methods = ['DELETE'])
def delete_cur_armory_account(id):
    armory = ArmoryAccounting.query.filter_by(id = id).first()

    db.session.delete(armory)
    db.session.commit()
    
    return {"message": "Success"}
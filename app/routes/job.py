from app import app, db
from flask import jsonify, request
from app.models import Job, JobSchema

@app.route('/job', methods = ['GET'])
def get_job():
    job_schema = JobSchema(many = True)

    req = Job.query.all()

    output = job_schema.dump(req)
    return jsonify(output)

@app.route('/job', methods = ['POST'])
def post_job():
    data = request.get_json()
    name = data['name']

    job = Job(name = name)
    db.session.add(job)
    db.session.commit()

    return {"message": "Success"}

@app.route('/job/<id>', methods = ['GET'])
def get_cur_job(id):
    job_schema = JobSchema(many = False)

    req = Job.query.filter_by(id = id).first()

    output = job_schema.dump(req)
    return jsonify(output)


@app.route('/job/<id>', methods = ['POST'])
def edit_cur_job(id):
    data = request.get_json()
    name = data['name']

    job = Job.query.filter_by(id = id).first()
    job.name = name
    db.session.commit()

    return {"message": "Success"}

@app.route('/job/<id>', methods = ['DELETE'])
def delete_cur_job(id):
    job = Job.query.filter_by(id = id).first()

    db.session.delete(job)
    db.session.commit()
    
    return {"message": "Success"}

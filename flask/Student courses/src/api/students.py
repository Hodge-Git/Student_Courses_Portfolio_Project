from flask import Blueprint, jsonify, abort, request
from ..models import Student, db, Account

bp = Blueprint('students', __name__, url_prefix = '/students')

@bp.route('', methods=['GET'])
def index():
    students = Student.query.all()
    result = []
    for s in students:
        result.append(s.serialize())
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def read(id: int):
    s = Student.query.get_or_404(id)
    return jsonify(s.serialize())

@bp.route('', methods=['POST'])
def create():
    if 'name' not in request.json:
        return abort(400)
    s = Student(
        name=request.json['name'],
    )

    db.session.add(s)
    db.session.commit()
    return jsonify(s.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id:int):
    s = Student.query.get_or_404(id)
    try:
        db.session.delete(s)
        db.session.commit() 
        return jsonify(True)
    except:
        return abort(500)

@bp.route('/<int:id>',methods=['PATCH','PUT'])
def update(id:int):
    s = Student.query.get_or_404(id)
    if 'name' not in request.json:
        return abort(400)
    else:
        s.name = request.json['name']
    try:
        db.session.commit()
        return jsonify(s.serialize())
    except:
        return abort(500)

@bp.route('/<int:id>/courses',methods=['GET'])
def get_courses(id:int):
    s = Student.query.get_or_404(id)
    result = []
    for c in s.courses:
        result.append(c.serialize())
    return jsonify(result)

@bp.route('/<int:id>/account',methods=['GET'])
def get_account(id:int):
    s = Student.query.get_or_404(id)
    if s.account is None:
        return abort(404)
    return jsonify(s.account.serialize())

@bp.route('/<int:id>/account', methods=['POST'])
def create_account(id:int):
    s = Student.query.get_or_404(id)
    if s.account is not None:
        return abort(400)

    if 'email' not in request.json:
        return abort(400)
    a = Account(
        email=request.json['email'],
        student_id = id
    )

    db.session.add(a)
    db.session.commit()
    return jsonify(a.serialize())

@bp.route('/find', methods=['GET'])
def find_account_by_email():
    if 'email' not in request.args:
        return abort(400)
    
    a = Account.query.filter_by(email=request.args['email']).first_or_404()

    return jsonify(a.student.serialize())
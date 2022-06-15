from ast import Not
from asyncio.windows_events import NULL
from flask import Blueprint, jsonify, abort, request
from ..models import Course, db

bp = Blueprint('courses', __name__, url_prefix = '/courses')

@bp.route('', methods=['GET'])
def index():
    courses = Course.query.all()
    result = []
    for c in courses:
        result.append(c.serialize())
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def read(id: int):
    c = Course.query.get_or_404(id)
    return jsonify(c.serialize())

@bp.route('', methods=['POST'])
def create():
    if 'name' not in request.json or 'course type' not in request.json:
        return abort(400)
    c = Course(
        name=request.json['name'],
        course_type = request.json['course type']
    )

    db.session.add(c)
    db.session.commit()
    return jsonify(c.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id:int):
    c = Course.query.get_or_404(id)
    try:
        db.session.delete(c)
        db.session.commit() 
        return jsonify(True)
    except:
        return abort(500)

@bp.route('/<int:id>',methods=['PATCH','PUT'])
def update(id:int):
    c = Course.query.get_or_404(id)
    if 'name' in request.json:
        c.name = request.json['name']
    if 'course type' in request.json:
        c.course_type = request.json['course type']
    
    try:
        db.session.commit()
        return jsonify(c.serialize())
    except:
        return abort(500)

@bp.route('/<int:id>/students',methods=['GET'])
def get_students(id:int):
    c = Course.query.get_or_404(id)
    result = []
    for s in c.students:
        result.append(s.serialize())
    return jsonify(result)

@bp.route('/<int:id>/exercise',methods=['GET'])
def get_excercises(id:int):
    c = Course.query.get_or_404(id)
    result = []
    for e in c.excercises:
        result.append(e.serialize())
    return jsonify(result)
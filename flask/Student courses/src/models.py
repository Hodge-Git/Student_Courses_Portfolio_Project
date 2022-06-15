from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Student_courses = db.Table('student_course',
    db.Column('student_id', db.ForeignKey('students.id'), primary_key=True),
    db.Column('course_id', db.ForeignKey('course.id'), primary_key=True)
)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(128))
    courses = db.relationship('Course', secondary = Student_courses)
    account = db.relationship('Account', back_populates= 'student', uselist = False)

    def serialize(self):
        return {
            'id':self.id,
            'name':self.name
        }


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(128), nullable = False)
    course_type = db.Column(db.String(128), nullable = False)
    students = db.relationship('Student', secondary = Student_courses)
    excercises = db.relationship('Excercise')

    def serialize(self):
        return {
            'id':self.id,
            'name':self.name,
            'course type':self.course_type
        }

class Excercise(db.Model):
    __tablename__='excercise'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(128), nullable = False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id') )

    def serialize(self):
        return {
            'id':self.id,
            'name':self.name
        }

class Account(db.Model):
    __tablename__='account'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(128), nullable = False, index = True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    student = db.relationship('Student', back_populates= 'account')

    def serialize(self):
        return {
            'id':self.id,
            'email':self.email
        }
from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from my_app import app

print(app)

db = SQLAlchemy(app)

class Course(db.Model):
    __tablename__ = "courses"
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(80), unique=True, nullable=False)
    
    def __init__(self, course_name):
        self.course_name = course_name

    @property
    def serialize(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name
        }

db.create_all()

@app.route("/courses/", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    return jsonify([course.serialize for course in courses])

@app.route("/courses/", methods=["POST"])
def create_course():
    new_course = Course(request.json['course_name'])
    db.session.add(new_course)
    db.session.commit()
    return jsonify(new_course.serialize)

@app.route("/courses/<int:id>/", methods = ["GET"])
def get_course(id):
    course = Course.query.get_or_404(id)
    return jsonify(course.serialize)

@app.route("/courses/<int:id>/", methods=["PUT", "PATCH"])
def update_course(id):
    course = Course.query.filter_by(course_id=id)
    course.update(dict(course_name = request.json["course_name"]))
    db.session.commit()
    return jsonify(course.first().serialize)

@app.route("/courses/<int:id>/", methods = ["DELETE"])
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return jsonify(course.serialize)


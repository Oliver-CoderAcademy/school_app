from flask import Blueprint, jsonify, request
from school_app import db
from school_app.models import Course

courses = Blueprint('courses', __name__)

@courses.route("/courses/", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    return jsonify([course.serialize for course in courses])

@courses.route("/courses/", methods=["POST"])
def create_course():
    new_course = Course(request.json['course_name'])
    db.session.add(new_course)
    db.session.commit()
    return jsonify(new_course.serialize)

@courses.route("/courses/<int:id>/", methods = ["GET"])
def get_course(id):
    course = Course.query.get_or_404(id)
    return jsonify(course.serialize)

@courses.route("/courses/<int:id>/", methods=["PUT", "PATCH"])
def update_course(id):
    course = Course.query.filter_by(course_id=id)
    course.update(dict(course_name = request.json["course_name"]))
    db.session.commit()
    return jsonify(course.first().serialize)

@courses.route("/courses/<int:id>/", methods = ["DELETE"])
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return jsonify(course.serialize)
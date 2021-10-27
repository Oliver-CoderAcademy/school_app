import os
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

(
    db_user, 
    db_pass, 
    db_name, 
    db_domain
) = (os.environ.get(item) for item in [
    "DB_USER", 
    "DB_PASS", 
    "DB_NAME", 
    "DB_DOMAIN"
    ]
)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_domain}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

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
    course = Course.query.get(id)
    if course:
        return jsonify(course.serialize)
    return jsonify(None)

@app.route("/courses/<int:id>/", methods=["PUT", "PATCH"])
def update_course(id):
    course = Course.query.filter_by(course_id=id)
    course.update(dict(course_name = request.json["course_name"]))
    db.session.commit()
    return jsonify(course.first().serialize)

@app.route("/courses/<int:id>/", methods = ["DELETE"])
def delete_course(id):
    course = Course.query.get(id)
    if course:
        db.session.delete(course)
        db.session.commit()
        return jsonify(course.serialize)
    abort(404)
    
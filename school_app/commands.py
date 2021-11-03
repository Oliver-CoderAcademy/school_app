from main import db
from flask import Blueprint

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables deleted")

@db_commands.cli.command("seed")
def seed_db():
    from models.courses import Course
    from faker import Faker
    faker = Faker()

    for i in range(20):
        course = Course(faker.catch_phrase())
        db.session.add(course)
    
    db.session.commit()
    print("Tables seeded")
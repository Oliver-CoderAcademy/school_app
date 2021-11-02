import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
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

    db.init_app(app)
    app.app_context().push()
    db.create_all()

    from controllers import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)

    return app


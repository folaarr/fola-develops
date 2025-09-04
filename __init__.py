# This module was created for database migrations
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import os
from dotenv import load_dotenv
from flask_migrate import Migrate



class Base(DeclarativeBase):
    pass

load_dotenv()

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    

    app.config["SECRET_KEY"] = os.environ.get("FLASK-SECRET-KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE-URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db) 

    # Import models so Alembic sees them
    from fola_develops_child.supplements import entities  

    return app
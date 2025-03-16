from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import Enum

db = SQLAlchemy()

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log = db.Column(db.String(1024))
    microservicio = db.Column(db.String(128))
    usuario = db.Column(db.String(128))

class LogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Log
        include_relationships = True
        load_instance = True
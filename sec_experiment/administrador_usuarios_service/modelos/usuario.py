from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy import Enum

db = SQLAlchemy()

class Rol(str, Enum):    
    CLIENTE = "CLIENTE"
    VENDEDOR = "VENDEDOR"
    ADMINISTRADOR = "ADMINISTRADOR"

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), unique=True)
    contrasena = db.Column(db.String(32))
    rol = db.Column(
        Enum(Rol.CLIENTE, Rol.VENDEDOR, Rol.ADMINISTRADOR, name="rol"),
        nullable=False
    )
    activo = db.Column(db.Boolean, default=True)

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True
        exclude = ('contrasena',)
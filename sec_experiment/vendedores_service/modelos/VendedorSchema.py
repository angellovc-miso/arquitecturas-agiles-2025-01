from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from .. import db

class Vendedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(32))
    ordenesPedido = db.relationship('OrdenPedido', back_populates='vendedor')

class VendedorSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "username")
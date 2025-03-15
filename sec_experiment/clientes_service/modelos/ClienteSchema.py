from flask_restful import Resource

from clientes_service import db

class Cliente(Resource):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(32))
    ordenesPedido = db.relationship('OrdenPedido', back_populates='cliente')

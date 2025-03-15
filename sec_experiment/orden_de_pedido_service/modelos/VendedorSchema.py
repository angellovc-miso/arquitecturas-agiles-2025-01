from flask_restful import Resource

from orden_de_pedido_service import db

class Vendedor(Resource):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(32))
    ordenesPedido = db.relationship('OrdenPedido', back_populates='vendedor')

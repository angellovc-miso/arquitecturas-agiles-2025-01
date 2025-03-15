import enum
from flask_restful import Resource
from orden_de_pedido_service import db

class TipoCliente(enum.Enum):
    FABRICANTE = 'FABRICANTE'
    TENDERO = 'TENDERO'
    SUPERMERCADO = 'SUPERMERCADO'
    MAYORISTA = 'MAYORISTA'

class Cliente(Resource):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(32))
    tipo = db.Column(db.Enum(TipoCliente))
    ordenesPedido = db.relationship('OrdenPedido')

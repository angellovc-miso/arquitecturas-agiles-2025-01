from flask_restful import Resource
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from orden_de_pedido_service import db
import enum

class Pago(enum.Enum):
    EFECTIVO = 'EFECTIVO'
    CONSIGNACION_BANCARIA = 'CONSIGNACION BANCARIA'
    CREDITO = 'CREDITO'
    CUOTAS = 'CUOTAS'
    TRANSFERENCIA = 'TRANSFERENCIA'

class EstadoPedido(enum.Enum):
    ABIERTO = 'ABIERTO'
    CERRADO = 'CERRADO'

class OrdenPedido(Resource):
    name: db.Column(db.String)
    ubicacion: db.Column(db.String)
    tipoDePago: db.Column(db.Enum(Pago))
    estado: db.Column(db.Enum(EstadoPedido))
    notas: db.Column(db.String)
    cliente: db.relationship('Cliente')

class OrdenPedidoSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = ["id", "name", "ubicacion", "tipoDePago", "estado", "notas"]

orden_pedido_schema = OrdenPedidoSchema()
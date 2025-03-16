from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.orm import Mapped, mapped_column
from .ClienteSchema import Cliente
from marshmallow import fields
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

class Pedido(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(db.String)
    tipoDePago: Mapped[str] = mapped_column(db.Enum(Pago))
    estado: Mapped[str] = mapped_column(db.Enum(EstadoPedido))
    cliente_id = mapped_column(db.Integer, db.ForeignKey("cliente.id"))
    # vendedor: db.relationship('Vendedor')

class OrdenPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ubicacion = db.Column(db.String, nullable=True)
    tipoDePago = db.Column(db.Enum(Pago))
    estado = db.Column(db.Enum(EstadoPedido))
    notas = db.Column(db.String, nullable=True)
    productos = db.Column(db.JSON, default=[])
    cliente_id = mapped_column(db.Integer, db.ForeignKey("cliente.id"))
    # cliente = db.relationship('Cliente')

class EnumMap(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {value.name: value.value}

class OrdenPedidoSchema(SQLAlchemyAutoSchema):
    tipoDePago = EnumMap(attribute=('tipoDePago'))
    estado = EnumMap(attribute=('estadoPedido'))
    class Meta:
        model = OrdenPedido
        include_relationships = True
        load_instance = True
        # fields = ["id", "name", "ubicacion", "tipoDePago", "estado", "notas", "productos"]



orden_pedido_schema = OrdenPedidoSchema(session=db.session)

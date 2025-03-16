from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .. import db
from sqlalchemy.orm import Mapped, mapped_column
from .ClienteSchema import Cliente
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

class OrdenPedidoSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = ["id", "name", "ubicacion", "tipoDePago", "estado", "notas"]

orden_pedido_schema = OrdenPedidoSchema()
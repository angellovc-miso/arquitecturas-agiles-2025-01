from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.orm import Mapped, mapped_column
from marshmallow import fields
from .. import db
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
    nombre: Mapped[str] = mapped_column(db.String, nullable=True)
    tipoDePago: Mapped[str] = mapped_column(db.Enum(Pago))
    estado: Mapped[str] = mapped_column(db.Enum(EstadoPedido))
    productos = db.Column(db.JSON, default=[])
    cliente_id = db.Column(db.Integer, nullable=False)
    vendedor_id = db.Column(db.Integer, nullable=True)

class EnumMap(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {value.name: value.value}

class OrdenPedidoSchema(SQLAlchemyAutoSchema):
    tipoDePago = EnumMap(attribute=('tipoDePago'))
    estado = EnumMap(attribute='estado')
    class Meta:
        model = Pedido
        load_instance = True


orden_pedido_schema = OrdenPedidoSchema(session=db.session)

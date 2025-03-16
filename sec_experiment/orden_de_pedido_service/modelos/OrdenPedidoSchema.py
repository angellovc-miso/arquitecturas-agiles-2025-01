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

from marshmallow import fields, ValidationError

class EnumMap(fields.Field):
    def __init__(self, enum, **kwargs):
        super().__init__(**kwargs)
        self.enum = enum

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.value  # Return only the value as a string

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return self.enum(value)
        except ValueError:
            raise ValidationError(f"Invalid value '{value}' for enum {self.enum.__name__}.")


class OrdenPedidoSchema(SQLAlchemyAutoSchema):
    tipoDePago = EnumMap(enum=Pago, attribute='tipoDePago')
    estado = EnumMap(enum=EstadoPedido, attribute='estado')
    class Meta:
        model = Pedido
        load_instance = True

orden_pedido_schema = OrdenPedidoSchema(session=db.session)

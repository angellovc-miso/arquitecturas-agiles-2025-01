from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .. import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Vendedor(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario: Mapped[str] = mapped_column(db.String)
    password: Mapped[str] = mapped_column(db.String(32))
    pedidos = relationship("Pedido")

class VendedorSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "username")
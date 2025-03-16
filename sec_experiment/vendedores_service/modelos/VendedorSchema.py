from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class VendedorSchema(SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "username")
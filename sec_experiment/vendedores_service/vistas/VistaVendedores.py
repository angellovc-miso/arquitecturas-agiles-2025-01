from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..modelos.OrdenPedidoSchema import Vendedor
from ..modelos.VendedorSchema import VendedorSchema
from .. import db

vendedor_schema = VendedorSchema()

class VistaVendedores(Resource):

    @jwt_required()
    def get(self):
        vendedores = Vendedor.query.all()
        return VendedorSchema.dump(vendedores)

    @jwt_required()
    def post(self):
        new_user = Vendedor(
            usuario=request.json['username'],
        )
        db.session.add(new_user)
        db.session.commit()
        return vendedor_schema.dump(new_user)
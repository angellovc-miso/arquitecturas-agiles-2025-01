from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..modelos.VendedorSchema import Vendedor, VendedorSchema
from .. import db

vendedor_schema = VendedorSchema()

class VistaVendedores(Resource):

    @jwt_required()
    def get(self):
        posts = Vendedor.query.all()
        return VendedorSchema.dump(posts)

    @jwt_required()
    def post(self):
        new_user = Vendedor(
            username=request.json['username'],
        )
        db.session.add(new_user)
        db.session.commit()
        return vendedor_schema.dump(new_user)
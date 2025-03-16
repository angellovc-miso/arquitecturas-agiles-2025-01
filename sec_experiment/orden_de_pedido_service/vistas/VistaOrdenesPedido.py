from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from flask import request
import requests

# from orden_de_pedido_service.modelos.OrdenPedidoSchema import Pedido, orden_pedido_schema
from orden_de_pedido_service.modelos.OrdenPedidoSchema import OrdenPedido, orden_pedido_schema, Pago, EstadoPedido
from orden_de_pedido_service import db
from flask_restful import Resource, reqparse
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError


url = 'http://127.0.0.1:5001'


class VistaOrdenesPedido(Resource):

    @jwt_required()
    def get(self):
        try:
            # Fetch all records from the database
            ordenes = db.session.query(OrdenPedido).all()
            # Serialize using Marshmallow schema

            # Validar token
            # headers = {
            #     'Authorization': f"{request.headers.get('Authorization')}"  # Aquí usamos el token que se pasó
            # }     
            # response = requests.get(url+"/ccpauth", headers=headers)
            # if response.status_code != 200:
            #     return {"msg": "Error de autenticación", "error": response.text}, 500
        
            result = [orden_pedido_schema.dump(orden) for orden in ordenes]
            return result, 200
        except SQLAlchemyError as e:
            print(e)
            return {"message": f"Database error: {str(e)}"}, 500


    def post(self):
        data = request.get_json()

        # Deserialize and validate incoming data
        try:
            new_order = orden_pedido_schema.load(data)
        except ValidationError as err:
            # Return validation errors
            print(err)
            return {"message": "Validation Error", "errors": err.messages}, 400

        try:
            db.session.add(new_order)
            db.session.commit()

            # Serialize the created object to return as response
            result = orden_pedido_schema.dump(new_order)

            return result, 201

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return {"message": f"Database error: {str(e)}"}, 500
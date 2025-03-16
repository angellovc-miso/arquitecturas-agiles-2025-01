from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from orden_de_pedido_service.modelos.OrdenPedidoSchema import OrdenPedido, orden_pedido_schema
from flask import request
import requests

url = 'http://127.0.0.1:5001'
# from orden_de_pedido_service.modelos.OrdenPedidoSchema import Pedido, orden_pedido_schema

class VistaOrdenesPedido(Resource):

    @jwt_required()
    def get(self):
        # [orden_pedido_schema.dump(pedido) for pedido in OrdenPedido.query.all()]

        # Validar token
        headers = {
            'Authorization': f'{request.headers.get('Authorization')}'  # Aquí usamos el token que se pasó
        }     
        response = requests.get(url+"/ccpauth", headers=headers)
        if response.status_code != 200:
            return {"msg": "Error de autenticación", "error": response.text}, 500
        
        return 'hello world'


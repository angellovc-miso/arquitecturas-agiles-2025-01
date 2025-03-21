from ..modelos.OrdenPedidoSchema import Pedido, orden_pedido_schema, Pago, EstadoPedido
from .. import db
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import requests
import json
import os

ENDPOINT_JWT = os.getenv("ENDPOINT_JWT", 'http://127.0.0.1:3001/ccpauth')
ENDPOINT_LOGS = os.getenv("ENDPOINT_LOGS", 'http://127.0.0.1:3003/log')
DETECTION_SERVICE_API = os.getenv("DETECTION_SERVICE_API", 'http://127.0.0.1:3004/detect_impersonation')


class VistaOrdenesPedido(Resource):

    @jwt_required()
    def get(self):
        usuario = json.loads(get_jwt_identity())  # Esto devuelve el diccionario completo

        # Extraer el nombre
        nombre =  usuario["nombre"]

        print(nombre)
        log = "El usuario " + nombre + " entró a ver órdenes de pedido"
        # Guardar logs
        response = requests.post(ENDPOINT_LOGS, json={"log": log, "microservicio": "orden_de_pedido_service", "usuario": nombre})

        # Validar token
        headers = {
            'Authorization': f"{request.headers.get('Authorization')}"  # Aquí usamos el token que se pasó
        }
        response = requests.get(ENDPOINT_JWT, headers=headers)
        if response.status_code != 200:
            return {"msg": "Error de autenticación", "error": response.text}, 500
        
        try:
            # Fetch all records from the database
            ordenes = db.session.query(Pedido).all()
            # Serialize using Marshmallow schema
            result = [orden_pedido_schema.dump(orden) for orden in ordenes]
            return result, 200
        except SQLAlchemyError as e:
            print(e)
            return {"message": f"Database error: {str(e)}"}, 500

    @jwt_required()
    def post(self):
        usuario = json.loads(get_jwt_identity())  # Esto devuelve el diccionario completo

        # Extraer el nombre
        nombre =  usuario["nombre"]

        print(nombre)
        log = "El usuario " + nombre + " entró a crear órdenes de pedido"
        # Guardar logs
        response = requests.post(ENDPOINT_LOGS, json={"log": log, "microservicio": "orden_de_pedido_service", "usuario": nombre})

        # Validar token
        headers = {
            'Authorization': f"{request.headers.get('Authorization')}"  # Aquí usamos el token que se pasó
        }
        response = requests.get(ENDPOINT_JWT, headers=headers)
        if response.status_code != 200:
            return {"msg": "Error de autenticación", "error": response.text}, 500

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
        

class VistaOrdenPedido(Resource):
    
    @jwt_required()
    def get(self, id):
        try:
            pedido = db.session.query(Pedido).filter(Pedido.id == id).first()
            if pedido:
                result = orden_pedido_schema.dump(pedido)
                return result, 200
            else:
                return {"message": "Pedido no encontrado"}, 404
        except SQLAlchemyError as e:
            print(e)
            return {"message": f"Database error: {str(e)}"}, 500

    @jwt_required()
    def put(self, id):
        try:
            user = json.loads(get_jwt_identity())  # Esto devuelve el diccionario completo
            # Validar token
            headers = {
                'Authorization': f"{request.headers.get('Authorization')}"  # Aquí usamos el token que se pasó
            }
            response = requests.get(ENDPOINT_JWT, headers=headers)
            if response.status_code != 200:
                return {"msg": "Error de autenticación", "error": response.text}, 500
    
            pedido = db.session.query(Pedido).filter(Pedido.id == id).first()
            if not pedido:
                return {"message": "Pedido not found"}, 404
            if pedido.estado is EstadoPedido.CERRADO and user['rol'] != 'ADMINISTRADOR':
                log = f"El usuario {user.get('nombre')} con rol {user.get('rol')} trató de editar la orden cerrada {pedido.id}"
                # Guardar logs
                response = requests.post(ENDPOINT_LOGS, json={"log": log, "microservicio": "orden_de_pedido_service", "usuario": user.get('nombre')})

                return {"message": "No puedes modificar pedidos cerrados"}, 403
            log = f"El usuario {user.get('nombre')} con rol {user.get('rol')} editó la orden {pedido.id} con status {pedido.estado}. La orden pertenece al vendedor {pedido.vendedor_id}"
            response = requests.post(ENDPOINT_LOGS, json={"log": log, "microservicio": "orden_de_pedido_service", "usuario": user.get('nombre')})
            requests.get(f"{DETECTION_SERVICE_API}?username={user.get('nombre')}")
            data = request.get_json()
            try:
                # Partial update (only update provided fields)
                updated_pedido = orden_pedido_schema.load(data, instance=pedido, partial=True)
            except ValidationError as err:
                print(err)
                return {"message": "Validation Error", "errors": err.messages}, 400

            db.session.commit()
            result = orden_pedido_schema.dump(updated_pedido)
            return result, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            print(e)
            return {"message": f"Database error: {str(e)}"}, 500

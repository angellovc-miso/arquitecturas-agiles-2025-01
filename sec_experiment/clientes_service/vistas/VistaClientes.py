from flask_restful import Resource

class VistaClientes(Resource):

    def get(self):

        return 'hello clientes'


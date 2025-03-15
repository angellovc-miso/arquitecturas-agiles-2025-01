from flask_restful import Resource
from orden_de_pedido_service.modelos.OrdenPedidoSchema import OrdenPedido, orden_pedido_schema

class VistaVendedores(Resource):

    def get(self):
        # [orden_pedido_schema.dump(pedido) for pedido in OrdenPedido.query.all()]

        return 'hello vendedores'


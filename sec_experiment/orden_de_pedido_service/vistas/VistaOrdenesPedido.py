from flask_restful import Resource
# from orden_de_pedido_service.modelos.OrdenPedidoSchema import Pedido, orden_pedido_schema

class VistaOrdenesPedido(Resource):

    def get(self):
        # [orden_pedido_schema.dump(pedido) for pedido in OrdenPedido.query.all()]

        return 'hello world'


from . import create_app, db
from flask_restful import Api
from flask_jwt_extended import JWTManager

from .modelos.OrdenPedidoSchema import Pedido
from .vistas.VistaOrdenesPedido import VistaOrdenesPedido, VistaOrdenPedido

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)

db.init_app(app)
db.create_all()

api.add_resource(VistaOrdenesPedido, '/pedidos')
api.add_resource(VistaOrdenPedido, '/pedido/<int:id>')

jwt = JWTManager(app)

with app.app_context():
    pedido_prueba = Pedido(
        nombre = 'cerveza',
        tipoDePago = 'EFECTIVO',
        estado = 'ABIERTO',
        cliente_id = 1
        # vendedor = 'pedroVendedor',
    )
    db.session.add(pedido_prueba)
    db.session.commit()

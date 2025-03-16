from flask_jwt_extended import JWTManager

from . import create_app, db
from flask_restful import Api

from .modelos.VendedorSchema import Vendedor
from .vistas.VistaVendedores import VistaVendedores

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)

db.init_app(app)
db.create_all()

api.add_resource(VistaVendedores, '/vendedores')
jwt = JWTManager(app)

with app.app_context():
    vendedor_prueba = Vendedor(username='pedroVendedor', password='12345')
    db.session.add(vendedor_prueba)
    db.session.commit()
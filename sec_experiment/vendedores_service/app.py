from vendedores_service import create_app, db
from flask_restful import Api
from vendedores_service.vistas.VistaVendedores import VistaVendedores

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)

db.init_app(app)
db.create_all()

api.add_resource(VistaVendedores, '/vendedores')
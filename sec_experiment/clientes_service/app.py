from clientes_service import create_app, db
from clientes_service.vistas.VistaClientes import VistaClientes
from flask_restful import Api

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)

db.init_app(app)
db.create_all()

api.add_resource(VistaClientes, '/clientes')
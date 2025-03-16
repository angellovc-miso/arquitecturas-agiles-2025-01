from . import create_app
from flask_restful import Resource, Api
from flask import request
from .modelos.log import Log, LogSchema
from .modelos import db

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)

class VistaLog(Resource):
    
    def post(self):
        
        nuevo_log = Log(log=request.json["log"], microservicio=request.json["microservicio"], usuario=request.json["usuario"])
        db.session.add(nuevo_log)
        db.session.commit()

        return {"mensaje": "Log creado exitosamente", "id": nuevo_log.id}
    
    def get(self):
        usuario = request.args.get('usuario')

        if usuario:
            logs = Log.query.filter_by(usuario=usuario).all()
        else:
            logs = Log.query.all()

        log_schema = LogSchema(many=True)
        return {"logs": log_schema.dump(logs)}

api.add_resource(VistaLog, '/log')
        
        
            
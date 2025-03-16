from administrador_usuarios_service import create_app
from flask_restful import Resource, Api
from flask import Flask, request
import hashlib
from flask_sqlalchemy import SQLAlchemy
from .modelos.usuario import Usuario, UsuarioSchema, Rol
from .modelos import db

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)

class VistaUsuario(Resource):
    
    def post(self):
        usuario = Usuario.query.filter(Usuario == request.json["nombre"]).first()
        if usuario is not None:
            return {"mensaje": "El usuario ya existe"}, 400

        # Obtener el rol del request, si no se proporciona, se asigna CLIENTE por defecto
        rol = request.json.get("rol")

        # Validar que el rol proporcionado sea válido
        if rol not in [Rol.CLIENTE, Rol.VENDEDOR, Rol.ADMINISTRADOR]:
            return {"mensaje": "Rol inválido."}, 400
        
        contrasena_encriptada = hashlib.md5(request.json["contrasena"].encode('utf-8')).hexdigest()
        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=contrasena_encriptada, rol=rol)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return {"mensaje": "Usuario creado exitosamente", "id": nuevo_usuario.id, "rol": nuevo_usuario.rol}
    
class VistaUsuarioObtener(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.nombre == request.json["nombre"], Usuario.contrasena == request.json["contrasena"]).first()
        if usuario is None:
            return {"mensaje": "El usuario no existe"}, 404
        return UsuarioSchema().dump(usuario)
    

api.add_resource(VistaUsuario, '/usuario/crear')
api.add_resource(VistaUsuarioObtener, '/usuario/obtener')
        
        
            
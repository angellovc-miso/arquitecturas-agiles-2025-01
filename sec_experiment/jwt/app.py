from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import hashlib
import requests
import jwt as jwt_lib

db = SQLAlchemy()
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secret-jwt"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
app.config["JWT_VERIFY_SUB"] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///revoked_tokens.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app_context = app.app_context()
app_context.push()

api = Api(app)

class RevokedTokens(db.Model):
    jti = db.Column(db.String(128), primary_key=True)
    nombre_usuario = db.Column(db.String(128))

db.init_app(app)
db.create_all()

jwt = JWTManager(app)


url = 'http://127.0.0.1:5000'

class AuthService(Resource):

    def post(self):
        response = requests.post(url+"/usuario/obtener", json={"nombre": request.json["nombre"], "contrasena": request.json['contrasena']})

        if response.status_code != 200:
            return {"mensaje": "El usuario no existe"}, 404
        
        usuario = response.json()
        print(usuario)

        token_de_acceso = create_access_token(identity=str({"id": usuario["id"], "rol": usuario["rol"]}))
        
        # Decodificar el token de acceso para obtener el 'jti'
        decoded_token = jwt_lib.decode(token_de_acceso, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])

        # Obtener el 'jti' del token decodificado
        jti = decoded_token['jti']
        
        db.session.add(RevokedTokens(jti=jti, nombre_usuario=usuario["nombre"]))
        db.session.commit()

        return {
            "mensaje": "Inicio de sesión exitoso",
            "token": token_de_acceso,
            "id": usuario["id"],
            "rol": usuario["rol"]
        }
    
    @jwt_required()
    def get(self):
        jti = get_jwt()['jti']  # El "jti" es el identificador único del token

        token = RevokedTokens.query.filter_by(jti=jti).first()
        if token is None:
            return {"mensaje": "Token inválido"}, 401
        return True, 200

class AuthServiceLogout(Resource):
   
        def post(self):
            nombre_usuario = request.json["nombre"]   
            tokens = RevokedTokens.query.filter_by(nombre_usuario=nombre_usuario).all()
            if tokens:
                for token in tokens:
                    db.session.delete(token)  # Eliminar cada token encontrado del usuario
                db.session.commit()  # Confirmar la transacción

            return {"mensaje": "Cierre de sesión exitoso"}

api.add_resource(AuthService, '/ccpauth')
api.add_resource(AuthServiceLogout, '/ccpauth/logout')

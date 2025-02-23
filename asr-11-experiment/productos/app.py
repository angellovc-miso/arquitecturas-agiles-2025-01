from . import create_app
from flask import jsonify
from flask_restful import Api, Resource
from healthcheck import HealthCheck, EnvironmentDump
import psutil
import os
import random
import flask_monitoringdashboard as dashboard
from faker import Faker
import time
import logging

fake = Faker()
ACCEPTED_CPU = os.getenv("ACCEPTED_CPU", float("90"))
ACCEPTED_MEMORY_RAM = os.getenv("ACCEPTED_MEMORY_RAM", float("90"))
ACCEPTED_DYSC = os.getenv("ACCEPTED_MEMORY_RAM", float("99.6"))
PROBABILIDAD = os.getenv("PROBABILIDAD", float("0.5"))

app = create_app('default')
app_context = app.app_context()
app_context.push()

health = HealthCheck()
envdump = EnvironmentDump()

api = Api(app)

class VistaProductos(Resource):
    def get(self):
        return {'productos': 'productos'}
    
api.add_resource(VistaProductos, '/productos')
    

# Agregar un chequeo básico de salud
@health.add_check
def basic_check():
    # Puedes poner cualquier lógica de monitoreo aquí
    # Por ejemplo, verificar si una base de datos está disponible o alguna otra condición
    """
    :param probabilidad_true: La probabilidad de que devuelva True (por ejemplo, 0.9 para 90%).
    :return: True o False según la probabilidad.
    """
    if random.random() < PROBABILIDAD:
        return True, "productos up"
    else:
        return False, "productos down"


@app.route('/')
def home():
    return "Microservicio funcionando correctamente"

@health.add_check
def check_system_health():
    # CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # Memory usage
    memory_info = psutil.virtual_memory()
    
    # Disk usage
    disk_usage = psutil.disk_usage('/')
    
    if cpu_usage > ACCEPTED_CPU or memory_info.percent > ACCEPTED_MEMORY_RAM or disk_usage.percent > ACCEPTED_DYSC:
        return False, {
            'cpu_usage': f'{cpu_usage}%',
            'memory_usage': f'{memory_info.percent}%',
            'disk_usage': f'{disk_usage.percent}%'
        }

    return True, {
        'cpu_usage': f'{cpu_usage}%',
        'memory_usage': f'{memory_info.percent}%',
        'disk_usage': f'{disk_usage.percent}%'
    }

app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())
dashboard.config.init_from(file='config.cfg')
dashboard.bind(app)

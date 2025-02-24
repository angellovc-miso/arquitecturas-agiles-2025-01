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
from datetime import timedelta, datetime
import logging

fake = Faker()
ACCEPTED_CPU = os.getenv("ACCEPTED_CPU", float("90"))
ACCEPTED_MEMORY_RAM = os.getenv("ACCEPTED_MEMORY_RAM", float("90"))
ACCEPTED_DYSC = os.getenv("ACCEPTED_MEMORY_RAM", float("99.6"))
PROBABILIDAD = os.getenv("PROBABILIDAD", float("0.7"))

app = create_app('default')
app_context = app.app_context()
app_context.push()

health = HealthCheck()
envdump = EnvironmentDump()

api = Api(app)

productos_slow_logs = []

class VistaProductos(Resource):
    def get(self):
        startTime = datetime.now()
        delay_ms = random.randint(5000, 6000)
        time.sleep(delay_ms / 1000.0)
        productos_list = []

        for item in range(random.randint(100, 500)):
            valor_unitario = random.randint(50, 100000)
            cantidad = random.randint(1, 1000)
            producto = {
                "nombre": fake.text(max_nb_chars=20),
                "fabricante": fake.company(),
                "sku": fake.sbn9(),
                "cantidad": cantidad,
                "valor_unitario": valor_unitario,
                "valor_al_por_mayor": valor_unitario * cantidad,
                "disponible": fake.pybool(),
                "es_alta_demanda": fake.pybool()
            }
            productos_list.append(producto)

        endTime = datetime.now()
        elapsedTime = endTime - startTime

        elapsedTime_ms = int(elapsedTime.total_seconds() * 1000)  # Convert to milliseconds

        log_entry = {
            'requestTime': startTime.isoformat(),
            'elapsedTime': elapsedTime_ms,
            'productsLength': len(productos_list)
        }

        if delay_ms > 5000:
            productos_slow_logs.append(log_entry)
            logging.warning(f"Request took {elapsedTime} ms, which is longer than expected.")
            # enviar mensaje por slack

        return jsonify(productos_list)

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

@health.add_check
def check_products_health():
    #  Si hay nuevas entradas en productos_slow_logs avisar al monitor
    now = datetime.now()

    if len(productos_slow_logs) == 0:
        return True, 'No hay demoras en la API de productos'

    latest_log_entry = productos_slow_logs[-1]
    latest_log_entry_failedTime = datetime.fromisoformat(latest_log_entry['requestTime'])
    thirty_seconds_before = now - timedelta(seconds=30)

    # Si la nueva entrada al log ocurrió en los ultimos 30 segundos devolver false
    if thirty_seconds_before <= latest_log_entry_failedTime <= now:
        return False, {
            'latest_response_time': latest_log_entry['elapsedTime'],
            'products_amount': latest_log_entry['productsLength']
        }
    else:
        return True, 'No hay demoras en la API de productos'

app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())

dashboard.config.init_from(file='config.cfg')
dashboard.bind(app)

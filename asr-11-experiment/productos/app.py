from productos import create_app
from flask_restful import Api, Resource
from healthcheck import HealthCheck, EnvironmentDump
import psutil

app = create_app('default')
app_context = app.app_context()
app_context.push()

health = HealthCheck()
envdump = EnvironmentDump()

api = Api(app)

ACCEPTED_PERCENTAGE = 80

class VistaProductos(Resource):
    def get(self):
        return {'productos': 'productos'}
    
api.add_resource(VistaProductos, '/productos')
    

# Agregar un chequeo básico de salud
@health.add_check
def basic_check():
    # Puedes poner cualquier lógica de monitoreo aquí
    # Por ejemplo, verificar si una base de datos está disponible o alguna otra condición
    return True, "productos ok"

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
    
    if cpu_usage > ACCEPTED_PERCENTAGE or memory_info.percent > ACCEPTED_PERCENTAGE or disk_usage.percent > ACCEPTED_PERCENTAGE:
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
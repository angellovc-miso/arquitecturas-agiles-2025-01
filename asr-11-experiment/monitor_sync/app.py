from . import create_app
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import time

app = create_app('default')
app_context = app.app_context()
app_context.push()

def check_health():
    try:
        print("Verificando estado del microservicio...")
        response = requests.get('http://127.0.0.1:5002/healthcheck')
        if response.status_code == 200:
            print("Microservicio funcionando correctamente.")
        else:
            print(f"Error al verificar el microservicio. Código de estado: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el microservicio: {e}")


# Configurar el scheduler
scheduler = BackgroundScheduler()

# Agregar un trabajo al scheduler para que ejecute check_health cada 30 segundos
scheduler.add_job(func=check_health, trigger="interval", seconds=30)

# Iniciar el scheduler en el primer request
@app.before_request
def start_scheduler():
    app.before_request_funcs[None].remove(start_scheduler)
    scheduler.start()
    
@app.route('/')
def home():
    return "Microservicio monitor funcionando correctamente."

if __name__ == '__main__':

    try:
        app.run(debug=True)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()  # Apagar el scheduler al terminar


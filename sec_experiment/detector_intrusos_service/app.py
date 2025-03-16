from detector_intrusos_service import create_app
from apscheduler.schedulers.background import BackgroundScheduler
import os
import random
import requests

app = create_app('default')
app_context = app.app_context()
app_context.push()

ENDPOINT_lOGS = os.getenv("ENDPOINT_lOGS", 'http://127.0.0.1:5002/logs')
ENDPOINT_LOGOUT = os.getenv("ENDPOINT_lOGS", 'http://127.0.0.1:5001/ccpauth/logout')

def check_logs():
    try:
        print("Verificando logs pedidos...")
        #response = requests.get(ENDPOINT_lOGS)
        validacion = False
        if random.random() < 0.7:
            validacion = True

        if validacion:
            usuario = "david"
            bloquear_usuario(usuario)

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el microservicio: {e}")

def bloquear_usuario(usuario):
    print(f"Bloqueando usuario: {usuario}")
    response = requests.post(ENDPOINT_LOGOUT, json={"nombre": usuario})
    if response.status_code == 200:
        print(f"Usuario {usuario} bloqueado correctamente.")
    else:
        print(f"Error al bloquear usuario {usuario}. Código de estado: {response.status_code}")
    


# Configurar el scheduler
scheduler = BackgroundScheduler()

# Agregar un trabajo al scheduler para que ejecute check_health cada 30 segundos
scheduler.add_job(func=check_logs, trigger="interval", seconds=30)


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

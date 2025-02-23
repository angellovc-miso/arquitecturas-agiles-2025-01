from . import create_app
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import time
import os
import json

ENDPOINT_PRODUCTOS = os.getenv("ENDPOINT_PRODUCTOS", 'http://127.0.0.1:5002/healthcheck')

app = create_app('default')
app_context = app.app_context()
app_context.push()


# URL del Webhook (reemplázala con tu URL)
webhook_url = 'https://hooks.slack.com/services/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'

# El mensaje que deseas enviar
mensaje = {
    "text": "¡Está fallando productos! por favor revisar. :warning:"
}


def check_health():
    try:
        print("Verificando estado del microservicio...")
        response = requests.get(ENDPOINT_PRODUCTOS)
        print(f"Estado del microservicio: {response.text}")
        if response.status_code == 200:
            print("Microservicio funcionando correctamente.")
        else:
            print(f"Error al verificar el microservicio. Código de estado: {response.status_code}")
            send_message_to_slack("Error al verificar el microservicio.")
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el microservicio: {e}")

def send_message_to_slack(message):
    # Enviar el mensaje a Slack
    response = requests.post(webhook_url, data=json.dumps(mensaje))

    # Verificar que el mensaje se haya enviado correctamente
    if response.status_code == 200:
        print("Mensaje enviado exitosamente.")
    else:
        print(f"Error al enviar mensaje de slack: {response.status_code}")

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


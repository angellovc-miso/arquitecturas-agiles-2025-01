from . import create_app
from apscheduler.schedulers.background import BackgroundScheduler
import os
import random
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = create_app('default')
app_context = app.app_context()
app_context.push()

ENDPOINT_lOGS = os.getenv("ENDPOINT_lOGS", 'http://127.0.0.1:5004/log')
ENDPOINT_LOGOUT = os.getenv("ENDPOINT_LOGOUT", 'http://127.0.0.1:5001/ccpauth/logout')
ENDPOINT_BLOQUEO = os.getenv("ENDPOINT_BLOQUEO", 'http://127.0.0.1:5000/usuario/bloquear')

def check_logs():
    try:
        print("Verificando logs pedidos...")
        response = requests.get(ENDPOINT_lOGS)
        data = response.json()

        # Extrae la lista de logs
        logs = data.get('logs', [])
        usuario_aleatorio = None
        if logs:
            print(f"Se encontraron {len(logs)} logs.")
            usuarios = [log['usuario'] for log in logs]  # Extrae todos los usuarios
            usuario_aleatorio = random.choice(usuarios)  # Selecciona un usuario aleatorio
        else:
            print("No hay logs disponibles.")

        validacion = False
        if random.random() < 0.7:
            validacion = True

        if validacion and usuario_aleatorio:
            usuario = usuario_aleatorio
            bloquear_usuario(usuario)
            enviar_correo(usuario)

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el microservicio: {e}")

def bloquear_usuario(usuario):
    print(f"Eliminando token de usuario: {usuario}")
    response = requests.post(ENDPOINT_LOGOUT, json={"nombre": usuario})
    if response.status_code == 200:
        print(f"Token de {usuario} borrado correctamente.")
    else:
        print(f"Error al eliminar el token usuario {usuario}. Código de estado: {response.status_code}")

    print(f"Bloqueando usuario: {usuario}")
    response = requests.put(ENDPOINT_BLOQUEO, json={"nombre": usuario})
    if response.status_code == 200:
        print(f"Usuario {usuario} bloqueado correctamente.")
    else:
        print(f"Error al bloquear el usuario {usuario}. Código de estado: {response.status_code}")
    

def enviar_correo(usuario):
    # Configuración de la cuenta de correo y servidor SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Puerto para TLS
    sender_email = "davids88899@gmail.com"  # Tu correo
    password = "qrrb ddny qwns yjjf"  # contraseña de aplicación
    receiver_email = "davids_8899@hotmail.com"  # Correo del destinatario

    # Crea el mensaje del correo
    subject = "Bloqueo de cuenta"
    body = "Alerta: acabamos de bloquear tu correo por detección de fraude."

    # Crear un objeto MIMEMultipart para el mensaje
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Agregar el cuerpo del mensaje al correo
    message.attach(MIMEText(body, "plain"))

    # Conectar al servidor SMTP y enviar el correo
    try:
        # Conexión con el servidor SMTP de Gmail
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Iniciar la encriptación TLS

        # Iniciar sesión en el servidor
        server.login(sender_email, password)

        # Enviar el correo
        server.sendmail(sender_email, receiver_email, message.as_string())

        print("Correo enviado con éxito")

    except Exception as e:
        print(f"Error al enviar el correo: {e}")

    finally:
        # Cerrar la conexión con el servidor SMTP
        server.quit()

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

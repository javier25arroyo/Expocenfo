import board
import time
import adafruit_hcsr04
import adafruit_mpu6050
import socketpool
import ssl
import wifi
import adafruit_requests as requests  # Agrega esta línea

socket = socketpool.SocketPool(wifi.radio)
https = requests.Session(socket, ssl.create_default_context())

print("Connecting...")
wifi.radio.connect("sspi", "password")
print("Connected to Wifi!")

URL = "http://api.open-notify.org/iss-now.json"

data = https.get(URL).json()
print(data)
long = data["iss_position"]["longitude"]
lat = data["iss_position"]["latitude"]
print(f"The International Space Station is located at {lat}, {long}")

# Configura el pin Trig y el pin Echo del sensor HC-SR04
trig = board.IO33
echo = board.IO27

# Crea un objeto HC-SR04
sonar = adafruit_hcsr04.HCSR04(trig, echo)

# Configura el objeto MPU6050
i2c = board.I2C()
mpu = adafruit_mpu6050.MPU6050(i2c)

# Variables para comparar la posición
distancia_anterior = 0

# Token del bot de Telegram
TELEGRAM_BOT_TOKEN = "6420443163:AAG0SXFNkEMq5sB2EPyabrY6S9mGPk7W808"
# ID de chat de Telegram
TELEGRAM_CHAT_ID = 5880741389  # Corrige la definición del ID de chat como un número entero

# Umbral de velocidad angular para detectar movimiento exponencial
UMBRAL_VELOCIDAD_ANGULAR = 50  # Puedes ajustar este valor según tu necesidad

def enviar_mensaje_telegram(mensaje):
    # Configuración de la conexión para enviar mensajes
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    parametros = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': mensaje
    }

    try:
        # Make the HTTP POST request with a timeout of 10 seconds
        response = adafruit_requests.post(url, json=parametros)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Mensaje enviado a Telegram")
        else:
            print(f"Error al enviar el mensaje a Telegram. Status code: {response.status_code}")

    except Exception as e:
        print(f"Error desconocido: {e}")

while True:
    try:
        # Medición de distancia con el sensor HC-SR04
        dist = sonar.distance

        # Verifica si la distancia ha cambiado
        if abs(dist - distancia_anterior) > 5:  # Puedes ajustar el umbral según tu necesidad
            mensaje = f"La posición ha cambiado. Nueva distancia: {dist} cm"
            enviar_mensaje_telegram(mensaje)

        # Actualiza la variable de distancia anterior
        distancia_anterior = dist

        # Lecturas del sensor MPU6050
        accel_x, accel_y, accel_z = mpu.acceleration
        gyro_x, gyro_y, gyro_z = mpu.gyro

        # Calcula la velocidad angular total
        velocidad_angular_total = abs(gyro_x) + abs(gyro_y) + abs(gyro_z)

        # Verifica si la velocidad angular supera el umbral
        if velocidad_angular_total > UMBRAL_VELOCIDAD_ANGULAR:
            mensaje_giroscopio = f"¡Movimiento exponencial detectado! Velocidad angular total: {velocidad_angular_total} grados/s"
            enviar_mensaje_telegram(mensaje_giroscopio)

        print("Aceleración (m/s^2):", accel_x, accel_y, accel_z)
        print("Direccion de la silla (grados/s):", gyro_x, gyro_y, gyro_z)
        print("Distancia:", dist)

    except RuntimeError as e:
        print(f"Error: {e}")

    except Exception as e:  # Agrega este bloque para manejar excepciones generales
        print(f"Error desconocido: {e}")

    time.sleep(0.5)
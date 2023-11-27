import board
import digitalio
import time
import adafruit_hcsr04
import adafruit_mpu6050
import wifi
import socketpool
import adafruit_requests
import simpleio

# Connect to Wi-Fi
wifi.radio.connect(ssid="2.4G_Home", password="23140815")

while True:
    try:
        # Check if the Wi-Fi connection is established
        if wifi.radio.ipv4_address:
            print("Connected to Wi-Fi")
            break
    except AttributeError:
        pass


print("Connected to Wi-Fi")

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
TELEGRAM_CHAT_ID = "5880741389"

def enviar_mensaje_telegram(mensaje):
    # Configuración de la conexión para enviar mensajes
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    parametros = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': mensaje
    }

    try:
        # Make the HTTP POST request
        response = adafruit_requests.post(url, json=parametros)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Mensaje enviado a Telegram")
        else:
            print(f"Error al enviar el mensaje a Telegram. Status code: {response.status_code}")

    except Exception as e:
        print(f"Error durante la solicitud HTTP: {e}")

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
        print("Aceleración (m/s^2):", accel_x, accel_y, accel_z)
        print("Direccion de la silla (grados/s):", gyro_x, gyro_y, gyro_z)
        print("Distancia:",dist)

    except RuntimeError as e:
        print(f"Error: {e}")

    time.sleep(0.5)
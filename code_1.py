import time
import board
import digitalio
import pulseio

TRIG_PIN = board.D13
ECHO_PIN = board.D12
PIEZO_PIN = board.D11

trig = digitalio.DigitalInOut(TRIG_PIN)
trig.direction = digitalio.Direction.OUTPUT

echo = digitalio.DigitalInOut(ECHO_PIN)
echo.direction = digitalio.Direction.INPUT

piezo = pulseio.PWMOut(PIEZO_PIN, duty_cycle=0, frequency=440, variable_frequency=True)

while True:
    duration, distance = 0, 0
    trig.value = False
    time.sleep(0.000002)
    trig.value = True
    time.sleep(0.00001)
    trig.value = False
    duration = pulseio.pulse_in(echo, True, 1000000)
    distance = duration / 29 / 2
    print("Distancia: ", distance, " cm")
    if distance >= 50 or distance <= 0:
        piezo.duty_cycle = 0
    elif distance >= 30:
        piezo.duty_cycle = 65535 // 2
        time.sleep(0.45)
        piezo.duty_cycle = 0
    elif distance >= 20:
        piezo.duty_cycle = 65535 // 2
        time.sleep(0.15)
        piezo.duty_cycle = 0
    elif distance >= 10:
        piezo.duty_cycle = 65535 // 2
        time.sleep(0.05)
        piezo.duty_cycle = 0
    else:
        piezo.duty_cycle = 65535 // 2
        time.sleep(0.15)
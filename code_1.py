import board
import digitalio
from time import sleep
import hcsr04
#from hcsr04 import HCSRO4

# Configura el pin Trig y el pin Echo del sensor HC-SR05
buzzer = digitalio.DigitalInOut(board.IO33)
trig = board.IO33
echo = board.IO27

# Crea un objeto HC-SR05
sonar = hcsr04.HCSR04(trig, echo)

while True:
    dist = sonar.dist_cm()
    print(dist)
    if dist >= 50 or dist <= 0:
        buzzer.value = False;
    elif dist >= 30:
        buzzer.value = True;
        sleep(0.45)
        buzzer.value = False;
    elif dist >= 20:
        buzzer.value = True;
        sleep(0.35)
        buzzer.value = False;
    elif dist >= 10:
        buzzer.value = True;
        sleep(0.25)
        buzzer.value = False;
    elif dist >= 5:
        buzzer.value = True;
        sleep(0.15)
        buzzer.value = False;
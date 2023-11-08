

import board
import digitalio
from time import sleep
import hcsr04
#from hcsr04 import HCSRO4

# Configura el pin Trig y el pin Echo del sensor HC-SR05
trig = board.IO33
echo = board.IO27

# Crea un objeto HC-SR05
sonar = hcsr04.HCSR04(trig, echo)

while True:
    dist = sonar.dist_cm()
    print(dist)
    sleep(0.5)
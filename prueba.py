import board
import digitalio
from time import sleep
import hcsr04

trig = board.IO33
echo = board.IO27

sonar = hcsr04.HCSR04(trig, echo)

while True:
    dist = sonsor.dist_cm()
    print(dist)
    if dist >= 50 or dist <= 0;
    
    sleep(0.5)
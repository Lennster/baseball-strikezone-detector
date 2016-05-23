#!/usr/bin/python

from gpiozero import LightSensor
from time import sleep
from gpiozero import LED

sensor = LightSensor(27,queue_len = 2)
redLed = LED(17)

strikes = 0
balls = 0
print("New batter")

while balls < 4 and strikes < 3:
    print("Pitch now. You have 5 seconds to pitch...")
    if sensor.wait_for_dark(5):
        strikes = strikes + 1
        print("Strike!")
    else:
        balls = balls + 1
        print("Ball :-(")

    print("Balls = %u; Strikes = %u" % (balls,strikes))
    sensor.wait_for_light()
    sleep(5)

if balls == 4:
    print("Walk to first")
else:
    print("Your out!!!")

#!/usr/bin/python

from gpiozero import LightSensor
from time import sleep
from signal import pause

horizSensor = LightSensor(27,queue_len = 2)
vertSensor = LightSensor(17,queue_len = 2)

class StrikeZone():
    def __init__(self):
        self.horizDetected = False
        self.vertDetected = False

    def horizDark(self, sensor):
        print("Detected dark on horiz sensor (Pin:%u)"%sensor.pin.number)
        self.horizDetected = True
        self.checkStrike()

    def horizLight(self,sensor):
        print("Detected light on horiz sensor (Pin:%u)"%sensor.pin.number)
        self.horizDetected = False

    def vertDark(self,sensor):
        print("Detected dark on vert sensor (Pin:%u)"%sensor.pin.number)
        self.vertDetected = True
        self.checkStrike()

    def vertLight(self,sensor):
        print("Detected light on vert sensor (Pin:%u)"%sensor.pin.number)
        self.vertDetected = False

    def checkStrike(self):
        if self.horizDetected and self.vertDetected:
            print("Strike")
        else:
            print("Ball")



try:
    detectZone = StrikeZone()
    while True:
        horizSensor.when_dark = detectZone.horizDark 
        horizSensor.when_light = detectZone.horizLight 
        vertSensor.when_dark = detectZone.vertDark
        vertSensor.when_light = detectZone.vertLight
        pause()
except KeyboardInterrupt:
    print("Exiting early,,,")


#!/usr/bin/python

from gpiozero import LightSensor
from time import sleep
from signal import pause

horizSensor = LightSensor(27,queue_len = 1, charge_time_limit = 0.01)
vertSensor = LightSensor(17,queue_len = 1,charge_time_limit = 0.01)

class StrikeZone():
    def __init__(self):
        self.horizDetected = False 
        self.vertDetected = False
        self.waitForOtherSensor = True
        self.clearingStrike = 0

    def horizDark(self, sensor):
        print("Detected dark on horiz sensor (Pin:%u)"%sensor.pin.number)
        self.horizDetected = True
        self.checkStrike()

    def vertDark(self,sensor):
        print("Detected dark on vert sensor (Pin:%u)"%sensor.pin.number)
        self.vertDetected = True
        self.checkStrike()

    def horizLight(self,sensor):
        print("Detected light on horiz sensor (Pin:%u)"%sensor.pin.number)
        self.horizDetected = False
        if self.clearingStrike == 0:
            self.checkStrike()
        else:
            self.clearingStrike = self.clearingStrike - 1

    def vertLight(self,sensor):
        print("Detected light on vert sensor (Pin:%u)"%sensor.pin.number)
        self.vertDetected = False
        if self.clearingStrike == 0:
            self.checkStrike()
        else:
            self.clearingStrike = self.clearingStrike - 1

    def checkStrike(self):
        if not self.waitForOtherSensor:
            if self.horizDetected and self.vertDetected:
                print("Strike")
                # Once we get a strike we need to wait for both sensors to go
                # back to light before checking for strikes or balls again
                self.clearingStrike = 2
            else:
                print("Ball")
            # Once we have determined it is a ball or strike need to go back to
            # wait for two triggers again
            self.waitForOtherSensor = True
        else:
            # Now we have detected one trigger lets just wait for one more
            self.waitForOtherSensor = False



try:
    detectZone = StrikeZone()
    horizSensor.when_dark = detectZone.horizDark 
    horizSensor.when_light = detectZone.horizLight 
    vertSensor.when_dark = detectZone.vertDark
    vertSensor.when_light = detectZone.vertLight
    pause()
except KeyboardInterrupt:
    print("Exiting early,,,")


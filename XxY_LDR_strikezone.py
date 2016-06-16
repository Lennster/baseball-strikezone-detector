#!/usr/bin/python

import unittest

from gpiozero import LightSensor
from gpiozero import RGBLED
from gpiozero import Button
from time import sleep

#Constants used within the script

# GPIO PINS
HORIZ_GPIO_PINS = [23,24,25,12,16] #GPIOs used for horizontal sensors, bottom to top
VERT_GPIO_PINS  = [17,27,22,5,6] #GPIOs used for vertical sensors, left to right
RGB_RED_PIN = 19
RGB_GREEN_PIN = 21
RGB_BLUE_PIN = 20
PITCH_BUTTON_PIN = 18

#SENSOR VALUES FOR TUNING SENSITIVITY
QUEUE_LEN = 1 # Capacitor must charge this many times to trigger dark
CHARGE_TIME = 0.010 #Value read must reach this value to count as one charge

# RGBLED COLORS
RED = (1,0,0)
GREEN = (0,1,0)
BLUE = (0,0,1)

#Globals
horizSensors = []
vertSensors = []

class StrikeZone():
    def __init__(self):
        self.waitForPitch = False
        self.resetBallsAndStrikes()

    def resetBallsAndStrikes(self):
        self.strikeCount = 0
        self.ballCount = 0

    def start(self):
        print "Ready to detect strikezone. Please pitch within the next 10 seconds."
        self.horizDetected = 0 
        self.vertDetected = 0
        self.waitForOtherSensor = True
        self.clearingStrike = 0
        self.waitForPitch = True
        rgbLed.color = GREEN

    def strike(self):
        self.strikeCount = self.strikeCount + 1
        rgbLed.color = RED
        self.isBatterOut()

    def ball(self):
        self.ballCount = self.ballCount + 1
        rgbLed.color = BLUE
        self.isBatterOut()

    def isBatterOut(self):
        self.waitForPitch = False
        print("Balls: %u, Strikes: %u" % (self.ballCount, self.strikeCount))
        if self.strikeCount == 3:
            print "Batter is out!!!"
            self.resetBallsAndStrikes()
        elif self.ballCount == 4:
            print "Batter walks to first base"
            self.resetBallsAndStrikes()

    def horizDark(self, sensor):
        print("Detected dark on horiz sensor (Pin:%u)"%sensor.pin.number)
        if self.waitForPitch:
            if self.horizDetected == 0:
                self.horizDetected = 1
                self.checkStrike()
            else:
                # Another horizontal sensor has been triggered - no need to check
                # for strike
                self.horizDetected = self.horizDetected + 1

    def vertDark(self,sensor):
        print("Detected dark on vert sensor (Pin:%u)"%sensor.pin.number)
        if self.waitForPitch:
            if self.vertDetected == 0:
                self.vertDetected = 1
                self.checkStrike()
            else:
                # Another vertical sensor has been triggered - no need to check for
                # strike
                self.vertDetected = self.vertDetected + 1

    def horizLight(self,sensor):
        print("Detected light on horiz sensor (Pin:%u)"%sensor.pin.number)
        if self.waitForPitch:
            if self.horizDetected > 0:
                self.horizDetected = self.horizDetected - 1

            if self.clearingStrike == 0:
                self.checkStrike()
            elif self.clearingStrike > 0:
                self.clearingStrike = self.clearingStrike - 1

    def vertLight(self,sensor):
        print("Detected light on vert sensor (Pin:%u)"%sensor.pin.number)
        if self.waitForPitch:
            if self.vertDetected > 0:
                self.vertDetected = self.vertDetected - 1

            if self.clearingStrike == 0:
                self.checkStrike()
            elif self.clearingStrike > 0:
                self.clearingStrike = self.clearingStrike - 1

    def checkStrike(self):
        if not self.waitForOtherSensor:
            if self.horizDetected and self.vertDetected:
                self.strike()
                # Once we get a strike we need to wait for both sensors to go
                # back to light before checking for strikes or balls again
                self.clearingStrike = 2
            else:
                self.ball()
            # Once we have determined it is a ball or strike need to go back to
            # wait for two triggers again
            self.waitForOtherSensor = True
        else:
            # Now we have detected one trigger lets just wait for one more
            self.waitForOtherSensor = False


if __name__ == "__main__":
    try:
        # Initialize RGB_LED
        rgbLed = RGBLED(RGB_RED_PIN, RGB_GREEN_PIN, RGB_BLUE_PIN, False)

        # Initialize the Pitch Button - this is used to start the timer. If a
        # ball or strike is not detected in time x after the button press the
        # pitch is considered a ball.
        pitchButton = Button(PITCH_BUTTON_PIN)

        # Create instance of StrikeZone
        detectZone = StrikeZone()

        #Now initialize sensors
        for index, horizPin in enumerate(HORIZ_GPIO_PINS):
            horizSensors.append(LightSensor(horizPin, 
                                            queue_len = QUEUE_LEN,
                                            charge_time_limit = CHARGE_TIME))
            horizSensors[index].when_dark = detectZone.horizDark 
            horizSensors[index].when_light = detectZone.horizLight 
        for index, vertPin in enumerate(VERT_GPIO_PINS):
            vertSensors.append(LightSensor(vertPin, 
                                           queue_len = QUEUE_LEN,
                                           charge_time_limit = CHARGE_TIME))
            vertSensors[index].when_dark = detectZone.vertDark
            vertSensors[index].when_light = detectZone.vertLight

        while True:
            if pitchButton.wait_for_press(10):
                #Button was pressed
                detectZone.start()
                sleep(1)
            elif detectZone.waitForPitch:
                # If ready for pitch but got timeout
                # Tell strikezone it was a ball an reset
                detectZone.ball()

    except KeyboardInterrupt:
        print("Thanks for playing...")


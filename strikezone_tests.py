#!/bin/user/python

import unittest
from XxY_LDR_strikezone import StrikeZone
from gpiozero import LightSensor

class TestStrikeZone(unittest.TestCase):
    def setUp(self):
        self.strikeZone = StrikeZone()
        self.horizSensor1 = LightSensor(17)
        self.horizSensor2 = LightSensor(27)
        self.vertSensor1 = LightSensor(23)
        self.vertSensor2 = LightSensor(24)

    def tearDown(self):
        self.horizSensor1.close()
        self.horizSensor2.close()
        self.vertSensor1.close()
        self.vertSensor2.close()
        self.strikeZone = None

    '''Test ball hitting horiz1 and not hitting either vertical'''
    def test_horizSensor1_ball(self):
        self.strikeZone.horizDark(self.horizSensor1)
        self.assertEquals(self.strikeZone.horizDetected,1)
        self.assertEquals(self.strikeZone.strikeCount,0)
        self.assertEquals(self.strikeZone.ballCount,0)

        self.strikeZone.horizLight(self.horizSensor1)
        self.assertEquals(self.strikeZone.strikeCount,0)
        self.assertEquals(self.strikeZone.ballCount,1)

    '''Test ball hitting vert1 and not hitting either horiz'''
    def test_vertSensor1_ball(self):
        self.strikeZone.vertDark(self.vertSensor1)
        self.assertEquals(self.strikeZone.vertDetected,1)
        self.assertEquals(self.strikeZone.strikeCount,0)
        self.assertEquals(self.strikeZone.ballCount,0)

        self.strikeZone.vertLight(self.vertSensor1)
        self.assertEquals(self.strikeZone.strikeCount,0)
        self.assertEquals(self.strikeZone.ballCount,1)

    '''Test ball hitting horiz1 and horiz2 and not hitting either vertical'''
    def test_horizSensor1_and_horiz2_ball(self):
        self.strikeZone.horizDark(self.horizSensor1)
        self.strikeZone.horizDark(self.horizSensor2)
        self.assertEquals(self.strikeZone.horizDetected, 2)
        self.assertEquals(self.strikeZone.strikeCount,0)
        self.assertEquals(self.strikeZone.ballCount,0)

        self.strikeZone.horizLight(self.horizSensor1)
        self.strikeZone.horizLight(self.horizSensor2)
        self.assertEquals(self.strikeZone.strikeCount,0)
        self.assertEquals(self.strikeZone.ballCount,1)

    '''Test ball hitting horiz1 and vert2 for strike'''
    def test_horizSensor1_and_vert2_strike(self):
        self.strikeZone.horizDark(self.horizSensor1)
        self.strikeZone.vertDark(self.vertSensor2)
        self.assertEquals(self.strikeZone.horizDetected, 1)
        self.assertEquals(self.strikeZone.vertDetected, 1)

        self.strikeZone.horizLight(self.horizSensor1)
        self.strikeZone.vertLight(self.vertSensor2)
        self.assertEquals(self.strikeZone.strikeCount,1)
        self.assertEquals(self.strikeZone.ballCount,0)



if __name__ == "__main__":
    unittest.main()

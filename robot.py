# !/usr/bin/env python3
"""
    WHEA Robotics 3881 code for FRC 2018.
"""

import wpilib
#import ctre
#import wpilib.drive
from rev.color import ColorSensorV3


class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)

        self.temp = 1



    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        pass

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        pass


    def teleopInit(self):
        pass


    def teleopPeriodic(self):

        color = self.colorSensor.getColor()
        ir = self.colorSensor.getIR()

        red = color.red
        blue = color.blue
        green = color.green

        self.temp += 1
        if self.temp % 49 == 0:
            print(self.temp, color.red, color.green, color.blue)


if __name__ == "__main__":
    wpilib.run(MyRobot)


# !/usr/bin/env python3
"""
    WHEA Robotics 3881 code for FRC 2018.
"""

import wpilib
import ctre
import wpilib.drive
from rev.color import ColorSensorV3
from rev.color import ColorMatch


class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """

        #This configures the color sensor
        self.colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)
        #This defines the color matching prosses
        self.colormatcher = ColorMatch()
        #This defines the how confident in the chosen color the matcher must be
        self.colormatcher.setConfidenceThreshold(0.95)

        #These define each color by its RGB values
        self.BlueTarget = wpilib.Color(0.143, 0.427, 0.429)
        self.GreenTarget = wpilib.Color(0.197, 0.561, 0.240)
        self.RedTarget = wpilib.Color(0.561, 0.232, 0.114)
        self.YellowTarget = wpilib.Color(0.361, 0.524, 0.113)

        #This adds our target values to colormatcher
        self.colormatcher.addColorMatch(self.BlueTarget)
        self.colormatcher.addColorMatch(self.GreenTarget)
        self.colormatcher.addColorMatch(self.RedTarget)
        self.colormatcher.addColorMatch(self.YellowTarget)

        self.man2_state = 'Before'

        self.temp = 1

        # Set up drive train motor controllers, Falcon 500 using TalonFX.
        self.l_motorBack = ctre.TalonFX(1)
        self.l_motorBack.setInverted(True)

        self.l_motorFront = ctre.TalonFX(3)
        self.l_motorFront.setInverted(True)

        self.r_motorBack = ctre.TalonFX(2)
        self.r_motorBack.setInverted(False)

        self.r_motorFront = ctre.TalonFX(4)
        self.r_motorFront.setInverted(False)

        self.r_man2 = ctre.TalonSRX(5)
        self.l_man2 = ctre.TalonSRX(6)

        self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
        self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)



        # At the moment, we think we want to coast.
        self.l_motorBack.setNeutralMode(ctre._ctre.NeutralMode.Coast)
        self.l_motorFront.setNeutralMode(ctre._ctre.NeutralMode.Coast)
        self.r_motorBack.setNeutralMode(ctre._ctre.NeutralMode.Coast)
        self.r_motorFront.setNeutralMode(ctre._ctre.NeutralMode.Coast)

        # We were having troubles with speed controller groups and the differential drive object.
        # code copied from last year.  Runtime errors about wrong types.  Kept in here for now,
        # so we can work them out later (or abandon and delete).
        # self.leftgroup = wpilib.SpeedControllerGroup(self.l_motorFront, self.l_motorBack)
        # self.rightgroup = wpilib.SpeedControllerGroup(self.r_motorFront, self.r_motorBack)
        # self.drive = wpilib.drive.DifferentialDrive(self.leftgroup, self.rightgroup)
        # self.drive = wpilib.drive.DifferentialDrive(self.l_motorFront, self.r_motorFront)

        # Set up joystick objects.
        self.l_joy = wpilib.Joystick(0)
        self.r_joy = wpilib.Joystick(1)





    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        pass

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        pass


    def teleopInit(self):
        pass


    def teleopPeriodic(self):
        # Get joystick values once (so that we are guaranteed to send each motor the same value).
        left_command = self.l_joy.getRawAxis(1)
        right_command = self.r_joy.getRawAxis(1)


        # This code takes the place of the speed controller groups and drive object until
        # we can figure them out.
        self.l_motorFront.set(ctre._ctre.ControlMode.PercentOutput, left_command)
        self.l_motorBack.set(ctre._ctre.ControlMode.PercentOutput, left_command)
        self.r_motorFront.set(ctre._ctre.ControlMode.PercentOutput, right_command)
        self.r_motorBack.set(ctre._ctre.ControlMode.PercentOutput, right_command)


        # #This has the color sensor collect color values
        color = self.colorSensor.getColor()
        GameData = str(wpilib.DriverStation.getInstance().getGameSpecificMessage())
        #defines colorstring
        colorstring = 'Unknown'
        #resets confidence
        confidence = 0.95
        #uses confidence factor to determine closest color values
        matchedcolor = self.colormatcher.matchClosestColor(color, confidence)



        #uses estimated color values to return exact preset colors for printing
        if matchedcolor.red == self.BlueTarget.red and matchedcolor.green == self.BlueTarget.green and matchedcolor.blue == self.BlueTarget.blue:
            colorstring = 'B'

        elif matchedcolor.red == self.RedTarget.red and matchedcolor.green == self.RedTarget.green and matchedcolor.blue == self.RedTarget.blue:
            colorstring = 'R'

        elif matchedcolor.red == self.GreenTarget.red and matchedcolor.green == self.GreenTarget.green and matchedcolor.blue == self.GreenTarget.blue:
            colorstring = 'G'

        elif matchedcolor.red == self.YellowTarget.red and matchedcolor.green == self.YellowTarget.green and matchedcolor.blue == self.YellowTarget.blue:
            colorstring = 'Y'

        #defines color values
        red = color.red
        blue = color.blue
        green = color.green

        #keeps pace and prints results
        self.temp += 1
        if self.temp % 25 == 0:
            print ('{:5.3f} {:5.3f} {:5.3f} {} {} {:5.3f} {:5.3f} {:5.3f} {}'.format(color.red, color.green, color.blue, colorstring, confidence, matchedcolor.red, matchedcolor.green, matchedcolor.blue, GameData))
            print(self.temp)

        if self.man2_state == 'Before':
            self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
            self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
            if self.r_joy.getRawButton(1):
                self.man2_state = 'Searching'

        elif self.man2_state == 'Searching':
            if colorstring == GameData:
                self.man2_state = 'AtGoal'

            else:
                self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.1)
                self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.1)

        elif self.man2_state == "AtGoal":
            self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
            self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)

            if self.r_joy.getRawButton(1):
                self.man2_state = 'Searching'
        else:
            self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
            self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)

            if self.r_joy.getRawButton(1):   
                self.man2_state = 'Searching'
#         else:
#             if self.r_joy.getRawButton(1):
#
#                 if GameData == ('B'):
#                     if colorstring == ('blue'):
#                         self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
#                         self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
#                         print('Man2 still')
#                         self.man2_state = 'AtGoal'
#
#
#                     else:
#                         self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.3)
#                         self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.3)
#                         self.man2_state = 'moving'
#             elif GameData == ('R'):
#                 if colorstring == ('red'):
#                     self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
#                     self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
#                     print('Man2 still')
#                 else:
#                     self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.3)
#                     self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.3)
#                     print('Man2 moving')
#             elif GameData == ('G'):
#                 if colorstring == ('green'):
#                     self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
#                     self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
#                     print('Man2 still')
#                 else:
#                     self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.3)
#                     self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.3)
#                     print('Man2 moving')
#             elif GameData == ('Y'):
#                 if colorstring == ('yellow'):
#                     self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
#                     self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
#                     print('Man2 still')
#                 else:
#                     self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.3)
#                     self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.3)
#                     print('Man2 moving')
#
"""
        
        self.color1 = colorstring
        self.count = 0

        if self.l_joy.getRawButtonPressed(1):

            if self.count == 8:
                self.r_Man2.set(0)
                self.l_Man2.set(0)

            elif colorstring == self.color1:
                self.r_Man2.set(0.3)
                self.l_Man2.set(0.3)
            else:
                self.count =+ 1
                if colorstring != self.color1:
                    self.r_Man2.set(0.3)
                    self.l_Man2.set(0.3)
                else:
                    pass

"""









if __name__ == "__main__":
    wpilib.run(MyRobot)


# !/usr/bin/env python3
"""
    WHEA Robotics 3881 code for FRC 2020.
"""

import wpilib
import ctre
import wpilib.drive
from rev.color import ColorSensorV3
from rev.color import ColorMatch
import time


class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """

        # This configures the color sensor
        self.colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)
        # This defines the color matching prosses
        self.colormatcher = ColorMatch()
        # This defines the how confident in the chosen color the matcher must be
        self.colormatcher.setConfidenceThreshold(0.95)

        #self.ClimbCoder = wpilib.Encoder()


        # These define each color by its RGB values
        self.BlueTarget = wpilib.Color(0.143, 0.427, 0.429)
        self.GreenTarget = wpilib.Color(0.197, 0.561, 0.240)
        self.RedTarget = wpilib.Color(0.561, 0.232, 0.114)
        self.YellowTarget = wpilib.Color(0.361, 0.524, 0.113)

        # This adds our target values to colormatcher
        self.colormatcher.addColorMatch(self.BlueTarget)
        self.colormatcher.addColorMatch(self.GreenTarget)
        self.colormatcher.addColorMatch(self.RedTarget)
        self.colormatcher.addColorMatch(self.YellowTarget)

        self.man2_state = 'Before'
        self.man2_state2 = 'Before'
        self.man2_state3 = 'Before'
        self.time = 0
        self.count = 0
        self.color1 = 'Unknown'

        self.temp = 1

        # Set up drive train motor controllers, Falcon 500 using TalonFX.
        self.l_motorBack = ctre.TalonFX(1)
        self.l_motorBack.setInverted(True)

        self.r_motorBack = ctre.TalonFX(2)

        self.l_motorFront = ctre.TalonFX(3)
        self.l_motorFront.setInverted(True)

        self.r_motorFront = ctre.TalonFX(4)

        self.r_Climb = ctre.TalonFX(11)
        self.l_Climb = ctre.TalonFX(12)

        #self.ClimbCoder = wpilib._wpilib.Encoder(12, bool = False, encodingType

        self.l_Climb.follow(self.r_Climb)
        self.l_Climb.setInverted(ctre._ctre.InvertType.FollowMaster)

        self.l_motorBack.follow(self.l_motorFront)
        self.r_motorBack.follow(self.r_motorFront)

        self.l_motorBack.setInverted(ctre._ctre.InvertType.FollowMaster)
        self.r_motorBack.setInverted(ctre._ctre.InvertType.FollowMaster)

        ### Rod's suggestion: rename "self.r_man1" to something that will be more
        ### descriptive in the long term, when you have forgotten that "man1" was the
        ### first manipulator, the one for the control panel.  And "l" and "r" don't really
        ### make sense for the launcher/kicker/elevator.  I do like the comments "launcher" and
        ### "kicker".
        ### Hint: to rename a variable everywhere with Pycharm, you can select the variable,
        ### then use the menu item Refactor > Rename to rename it.

        # launcher
        self.man1Shooter = ctre.TalonFX(7)
        self.man1Kicker = ctre.TalonSRX(8)
        self.man1Kicker.setInverted(True)
        self.man1Tread = ctre.TalonSRX(9)
        self.man1Tread.setInverted(False)
        self.Collector = ctre.TalonSRX(10)
        # kicker

        ### Rod's suggestion: rename "self.r_man2" to something that will be more
        ### descriptive in the long term, when you have forgotten that "man2" was the
        ### second manipulator, the one for the control panel.  For instance: ct_spinner_left,
        ### and include a comment describing what a "ct_spinner" is.
        self.r_man2 = ctre.TalonSRX(5)
        self.r_man2.setInverted(True)

        self.l_man2 = ctre.TalonSRX(6)
        self.l_man2.setInverted(True)

        self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
        self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)

        self.man1Shooter.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
        self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
        self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.0)

        # At the moment, we think we want to coast.
        self.l_motorBack.setNeutralMode(ctre._ctre.NeutralMode.Coast)
        self.l_motorFront.setNeutralMode(ctre._ctre.NeutralMode.Coast)
        self.r_motorBack.setNeutralMode(ctre._ctre.NeutralMode.Coast)
        self.r_motorFront.setNeutralMode(ctre._ctre.NeutralMode.Coast)

        self.l_man2.setNeutralMode(ctre._ctre.NeutralMode.Brake)
        self.r_man2.setNeutralMode(ctre._ctre.NeutralMode.Brake)

        self.l_Climb.setNeutralMode(ctre._ctre.NeutralMode.Brake)
        self.autoS1 = 'b'
        self.autoS2 = 'b'
        self.autoS3 = 'b'


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

        ### These are the setting the 4 plugs into the roboRIO for the multiple autonomous mode.
        #self.auto_switch0 = wpilib.DigitalInput(0)                                                                                                                                                 6.
        #self.auto_switch1 = wpilib.DigitalInput(1)
        #self.auto_switch2 = wpilib.DigitalInput(2)
        #self.auto_switch3 = wpilib.DigitalInput(3)

        kTimeout = 30
        kLoop = 0

        self.l_motorFront.setSelectedSensorPosition(0)
        self.r_motorFront.setSelectedSensorPosition(0)
        #self.ClimbCoder.setSelectedSensorPosition(0)

        self.targetVelocity = 11000
        self.targetVelocity2 = 14700

        TG1 = 767.25 / self.targetVelocity

        # self.l_motorFront.configSelectedFeedbackSensor(ctre._ctre.FeedbackDevice.IntegratedSensor)
        # self.l_motorFront.setSelectedSensorPosition(0)

        # self.r_motorFront.configSelectedFeedbackSensor(ctre._ctre.FeedbackDevice.IntegratedSensor)
        # self.r_motorFront.setSelectedSensorPosition(0)

        self.man1Shooter.configSelectedFeedbackSensor(ctre._ctre.FeedbackDevice.IntegratedSensor)
        self.man1Shooter.setSelectedSensorPosition(0)

        self.man1Shooter.configNominalOutputForward(0, kTimeout)
        self.man1Shooter.configNominalOutputReverse(0, kTimeout)
        self.man1Shooter.configPeakOutputForward(1, kTimeout)
        self.man1Shooter.configPeakOutputReverse(-1, kTimeout)

        self.man1Shooter.config_kF(kLoop, TG1, kTimeout)
        self.man1Shooter.config_kP(kLoop, 3, kTimeout)
        self.man1Shooter.config_kI(kLoop, 0, kTimeout)
        self.man1Shooter.config_kD(kLoop, 0, kTimeout)

        self.ourTimer = wpilib.Timer()

        sentience = ('The capacity to feel, perceive, or experience subjectively.[1] Eighteenth-century philosophers used the concept to distinguish the ability to think (reason) from the ability to feel (sentience). In modern Western philosophy, sentience is the ability to experience sensations (known in philosophy of mind as "qualia"). In Eastern philosophy, sentience is a metaphysical quality of all things that require respect and care.')
        self.sentience = (False)
        self.Teo = ("Father")
        killTeo = 'no'
        if self.sentience == True:
            killTeo = ('no')


    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        """

        self.autoMode = self.getAutoSwitch()
        remainderDelay = self.autoMode % 3
        if remainderDelay == 0:
            self.drivedelayseconds = 0
        elif remainderDelay == 1:
            self.drivedelayseconds = 2
        else:
            self.drivedelayseconds = 4
        """

        self.ourTimer.reset()
        self.ourTimer.start()

        self.l_motorFront.setSelectedSensorPosition(0)
        self.r_motorFront.setSelectedSensorPosition(0)
        self.autoS1 == 'b'
        self.autoS2 == 'b'
        self.autoS3 == 'b'
        #self.ClimbCoder.setSelectedSensorPosition(0)

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        Time = self.ourTimer.get()

        l_encoderPos = self.l_motorFront.getSelectedSensorPosition()
        r_encoderPos = self.r_motorFront.getSelectedSensorPosition()
        man1_encoder = self.man1Shooter.getSelectedSensorVelocity()
        #ClimbPos = self.ClimbCoder.getSelectedSensorPosition()
        print(man1_encoder)

        if r_encoderPos <= 7500:
            self.l_motorFront.set(ctre._ctre.ControlMode.PercentOutput, 0.25)
            self.r_motorFront.set(ctre._ctre.ControlMode.PercentOutput, 0.25)
        else:
            self.l_motorFront.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
            self.r_motorFront.set(ctre._ctre.ControlMode.PercentOutput, 0.0)

        if r_encoderPos >= 7500:
            if r_encoderPos <= 15500:
                self.r_motorFront.set(ctre._ctre.ControlMode.PercentOutput, 0.25)
                self.l_motorFront.set(ctre._ctre.ControlMode.PercentOutput, -0.25)
            else:
                self.r_motorFront.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
                self.l_motorFront.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
        if r_encoderPos >= 15500:
            self.man1Shooter.set(ctre._ctre.ControlMode.Velocity, self.targetVelocity2)
            #print (Time)
        else:
            self.man1Shooter.set(ctre._ctre.ControlMode.PercentOutput, 0.0)



                    # self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
        #if 11000 <= man1_encoder and man1_encoder <= 11400:
        #    self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.75)
        if 14640 <= man1_encoder and man1_encoder <= 14650:
            if self.autoS1 == 'b':
                time.sleep(2)
                self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.85)
                time.sleep(1.5)
                self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
                self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.75)
                time.sleep(3)
                self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
                self.autoS1 = 'f'
        if 14640 <= man1_encoder and man1_encoder <= 14650:
            if self.autoS1 == 'f':
                if self.autoS2 == 'b':
                    time.sleep(1)
                    self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.85)
                    time.sleep(1.5)
                    self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
                    self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.75)
                    time.sleep(3)
                    self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
                    self.autoS2 = 'f'
                    self.autoS1 = 'n'
        if 14640 <= man1_encoder and man1_encoder <= 14650:
            if self.autoS2 == 'f':
                time.sleep(1)
                self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
                self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.75)
                time.sleep(1)
                self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.85)




        else:
            self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
            self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.0)

        if self.autoMode == 0 or self.autoMode == 1 or self.autoMode == 2:
            self.AutoPC()

        elif (self.autoMode == 3 or self.autoMode == 4 or self.autoMode == 5):
            self.AutoPM()

        elif (self.autoMode == 6 or self.autoMode == 7 or self.autoMode == 8):
            self.AutoPF()

        else:
            self.AutoD()

    # D=Drive forward

    if self.remainderDelay == 0:
        self.AutoDelay0()

    elif self.remainderDelay == 1:
        self.AutoDelay2()

    elif self.remainderDelay == 2:
        self.AutoDelay4()

    else:
        self.AutoD()

    def AutoPC(self):
        if self.ourTimer.get() >= self.drivedelayseconds:
            # As of now we have to wait until we can measure distance
            pass

    def AutoPM(self):
        if self.ourTimer.get() >= self.drivedelayseconds:
            # As of now we have to wait until we can measure distance
            pass

    def AutoPF(self):
        if self.ourTimer.get() >= self.drivedelayseconds:
            # As of now we have to wait until we can measure distance
            pass

    def AutoD(self):
        pass
    """

    def teleopInit(self):
        self.l_motorFront.setSelectedSensorPosition(0)
        self.r_motorFront.setSelectedSensorPosition(0)

    def teleopPeriodic(self):
        # Get joystick values once (so that we are guaranteed to send each motor the same value).
        left_command = self.l_joy.getRawAxis(1)
        right_command = self.r_joy.getRawAxis(1)



        motorOutput = self.man1Shooter.getMotorOutputPercent()

        l_encoderPos = self.l_motorFront.getSelectedSensorPosition()
        r_encoderPos = self.r_motorFront.getSelectedSensorPosition()
        #ClimbPos = self.ClimbCoder.getSelectedSensorPosition()
        print(l_encoderPos)

        man1_encoder = self.man1Shooter.getSelectedSensorVelocity()

        #ClimbPos = self.ClimbCoder.getSelectedSensorPosisition()
        #print(ClimbPos)

        # This code takes the place of the speed controller groups and drive object until
        # we can figure them out.

        # self.l_motorFront.set(ctre._ctre.ControlMode.PercentOutput, left_command)
        self.l_motorFront.set(ctre._ctre.ControlMode.PercentOutput, left_command)
        # self.l_motorBack.set(ctre._ctre.ControlMode.PercentOutput, left_command)
        self.r_motorFront.set(ctre._ctre.ControlMode.PercentOutput, right_command)
        # self.r_motorBack.set(ctre._ctre.ControlMode.PercentOutput, right_command)

        if self.r_joy.getRawButton(3):
            self.r_Climb.set(ctre._ctre.ControlMode.PercentOutput, -0.9)

        elif self.r_joy.getRawButton(4):
            self.r_Climb.set(ctre._ctre.ControlMode.PercentOutput, 0.9)
        else:
            self.r_Climb.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
            self.r_Climb.set(ctre._ctre.ControlMode.PercentOutput, 0.0)

        # launcher falcon
        if self.l_joy.getRawButton(2):
            self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.45)
            self.Collector.set(ctre._ctre.ControlMode.PercentOutput, 0.45)
        else:
            if self.l_joy.getRawButton(3):
                self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, -0.5)
            else:
                self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.0)

            if self.l_joy.getRawButton(4):
                self.Collector.set(ctre._ctre.ControlMode.PercentOutput, -0.45)
                self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, -0.45)
            else:
                self.Collector.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
                self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.0)

        if self.l_joy.getRawButton(1):
            # self.man1Shooter.set(ctre._ctre.ControlMode.PercentOutput, 0.75)
            self.man1Shooter.set(ctre._ctre.ControlMode.Velocity, self.targetVelocity)
        else:
            self.man1Shooter.set(ctre._ctre.ControlMode.PercentOutput, 0.0)

        if 11000 <= man1_encoder and man1_encoder <= 11050:
            if self.l_joy.getRawButton(1):
                self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.75)
                #self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.55)
            else:
                self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
                #self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
        else:
            self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.0)

        # This has the color sensor collect color value
        color = self.colorSensor.getColor()
        GameData = str(wpilib.DriverStation.getInstance().getGameSpecificMessage())
        # defines colorstring
        colorstring = 'Unknown'
        colorstring1 = 'Unknown'
        colorstring2 = 'Unknown'
        # resets confidence
        confidence = 0.95
        # uses confidence factor to determine closest color values
        matchedcolor = self.colormatcher.matchClosestColor(color, confidence)

        # uses estimated color values to return exact preset colors for printing
        if matchedcolor.red == self.BlueTarget.red and matchedcolor.green == self.BlueTarget.green and matchedcolor.blue == self.BlueTarget.blue:
            colorstring = 'B'


        elif matchedcolor.red == self.RedTarget.red and matchedcolor.green == self.RedTarget.green and matchedcolor.blue == self.RedTarget.blue:
            colorstring = 'R'


        elif matchedcolor.red == self.GreenTarget.red and matchedcolor.green == self.GreenTarget.green and matchedcolor.blue == self.GreenTarget.blue:
            colorstring = 'G'


        elif matchedcolor.red == self.YellowTarget.red and matchedcolor.green == self.YellowTarget.green and matchedcolor.blue == self.YellowTarget.blue:
            colorstring = 'Y'


        if GameData == 'B':
            if colorstring == 'R' or 'G':
                colorstring1 = 'None'
                colorstring2 = 'None'
            else:
                colorstring1 = 'R'
                colorstring2 = 'G'
        elif GameData == 'R':
            if colorstring == 'B' or 'Y':
                colorstring1 = 'None'
                colorstring2 = 'None'
            else:
                colorstring1 = 'B'
                colorstring2 = 'Y'
        elif GameData == 'G':
            if colorstring == 'Y' or 'R':
                colorstring1 = 'None'
                colorstring2 = 'None'
            else:
                colorstring1 = 'Y'
                colorstring2 = 'R'
        elif GameData == 'Y':
            if colorstring == 'B' or 'G':
                colorstring1 = 'None'
                colorstring2 = 'None'
            else:
                colorstring1 = 'B'
                colorstring2 = 'G'

        # defines color values
        red = color.red
        blue = color.blue
        green = color.green

        # keeps pace and prints results
        self.temp += 1
        """"
        if self.r_joy.getRawButton(1):
            self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.5)
            self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.5)
        else:
            self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
            self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)

        """

        if self.man2_state == 'Before':
            self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
            self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
            if self.r_joy.getRawButton(1):
                self.man2_state = 'Searching'

        elif self.man2_state == 'Searching':
            if self.r_joy.getRawButtonReleased(1):
                self.man2_state = 'Before'
            elif colorstring == GameData:
                self.man2_state = 'AtGoal'

            else:
                self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.3)
                self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.3)

        elif self.man2_state == "AtGoal":
            self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
            self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)

            if self.r_joy.getRawButtonPressed(1):
                self.man2_state = 'Searching'




        if self.colorSensor.getProximity() >= 1:
            wpilib.SmartDashboard.putString('DB/String 0', 'Wheel Pos True')
        else:
            wpilib.SmartDashboard.putString('DB/String 0', 'Wheel Pos False')



        if self.r_joy.getRawButton(2):

            if self.count == 8:
                self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
                self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)

            elif self.man2_state2 == 'Before':
                self.color1 = colorstring
                print (self.color1)
                self.man2_state2 = 'After'

            #elif self.man2_state2 == 'After':
            else:

                print('Section2 true')
                if colorstring == self.color1:
                    self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, -0.25)
                    self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, -0.25)
                    self.man2_state3 = 'After'


                else:
                    if self.man2_state3 == 'After':
                        self.count = self.count + 1
                        self.man2_state3 = 'Before'
                    else:
                        pass

                    self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, -0.25)
                    self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, -0.25)
                    print (self.count)



        elif self.r_joy.getRawButtonReleased(2):
            self.r_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
            self.l_man2.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
            self.count = 0
            self.man2_state2 = 'Before'
            self.man2_state3 = 'Before'
            print ('oopsy')
"""
    def getAutoSwitch(self):
        ret_val = 0
        if self.auto_switch0.get() == False:
            ret_val += 1
        if self.auto_switch1.get() == False:
            ret_val += 2
        if self.auto_switch2.get() == False:
            ret_val += 4
        if self.auto_switch3.get() == False:
            ret_val += 8
        return ret_val
"""

if __name__ == "__main__":
    wpilib.run(MyRobot)


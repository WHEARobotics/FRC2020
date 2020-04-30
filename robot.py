# !/usr/bin/env python3
"""
    WHEA Robotics 3881 code for FRC 2020.
"""

#==>> Rod's comments 2020-03-07 preceeded by the wide arrow.

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
<<<<<<< Updated upstream


        self.BlueTarget = wpilib.Color(0.143, 0.427, 0.429)
        self.GreenTarget = wpilib.Color(0.197, 0.561, 0.240)
        self.RedTarget = wpilib.Color(0.561, 0.232, 0.114)
        self.YellowTarget = wpilib.Color(0.361, 0.524, 0.113)
<<<<<<< Updated upstream

        # This adds our target values to colormatcher
        self.colormatcher.addColorMatch(self.BlueTarget)
        self.colormatcher.addColorMatch(self.GreenTarget)
        self.colormatcher.addColorMatch(self.RedTarget)
        self.colormatcher.addColorMatch(self.YellowTarget)
<<<<<<< Updated upstream
=======

        self.man2_state = 'Before'
        self.man2_state2 = 'Before'
        self.man2_state3 = 'Before'
        self.time = 0
        self.count = 0
        self.color1 = 'Unknown'
        self.temp = 1
        ColorWheel = ''

        # ==>> We are not currently using this variable, except to increment it in teleopPeriodic().
        # ==>> Originally, it helped slow down printing.  If we aren't going to use it, we should
        # ==>> just delete it here and in teleopPeriodic().


        # Set up drive train motor controllers, Falcon 500 using TalonFX.
        self.l_motorBack = ctre.TalonFX(1)
        self.l_motorBack.setInverted(True)

        self.r_motorBack = ctre.TalonFX(2)

        self.l_motorFront = ctre.TalonFX(3)
        self.l_motorFront.setInverted(True)

        self.r_motorFront = ctre.TalonFX(4)

        # ==>> Shouldn't these be TalonSRX?  TalonFX is for the Falcons.
        # ==>> They are very similar, but not identical.
        self.r_Climb = ctre.TalonSRX(11)
        self.l_Climb = ctre.TalonSRX(12)

        # ==>> See Rod's post in the #programming Slack channel on Thursday, 2020-03-05.
        # ==>> I made some suggestions about how we might get the climber encoder working
        # ==>> based on previous years' code.
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

        #Teo: That command didnt work for me... maybe I was using it wrong?

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

        # ==>> We should set the right climb to brake as well.
        self.l_Climb.setNeutralMode(ctre._ctre.NeutralMode.Brake)
        self.r_Climb.setNeutralMode(ctre._ctre.NeutralMode.Brake)

        # ==>> It would be really helpful to add comments that explain what these variables
        # ==>> are for, and what their legal values are.

        #Configures Autonomous State Variables
        self.autoS1 = 'b'
        self.autoS2 = 'b'
        self.autoS3 = 'b'

        #Configures autonomous Stage Variable, Starting at '1'
        self.autoStage = '1'



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


        # These are the setting the 4 plugs into the roboRIO for the multiple autonomous mode.
        self.auto_switch0 = wpilib.DigitalInput(0)
        self.auto_switch1 = wpilib.DigitalInput(1)
        self.auto_switch2 = wpilib.DigitalInput(2)
        self.auto_switch3 = wpilib.DigitalInput(3)

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



        self.ourTimer.reset()
        self.ourTimer.start()

        self.l_motorFront.setSelectedSensorPosition(0)
        self.r_motorFront.setSelectedSensorPosition(0)
        self.autoS1 = 'b'
        self.autoS2 = 'b'
        self.autoS3 = 'b'
        self.autoStage = '1'
        self.autoMode = self.getAutoSwitch()
        motorState = 'off'
        #self.ClimbCoder.setSelectedSensorPosition(0)

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        Time = self.ourTimer.get()

        l_encoderPos = self.l_motorFront.getSelectedSensorPosition()
        r_encoderPos = self.r_motorFront.getSelectedSensorPosition()
        man1_encoder = self.man1Shooter.getSelectedSensorVelocity()
        #ClimbPos = self.ClimbCoder.getSelectedSensorPosition()

        # ==>> Rod recommends changing from print statements to using the SmartDashboard.
        #Teo says: I dont know how to do that yet but ill put it on my list
        print(man1_encoder)

        if self.autoStage =='1':
            if self.autoMode == 0 or self.autoMode == 1 or self.autoMode == 2:
                self.autoStage = '2'
            elif self.autoMode == 3 or self.autoMode == 4:
                time.sleep(3)
                self.autoStage = '2'
        # ==>> I think this next line would be better as an "elif", to make it clear that
        # ==>> you are exhaustively going through the possible values of self.autoStage.
        elif self.autoStage =='2':
            if self.autoMode == 0:
                if r_encoderPos <= 7500:
                    self.l_motorFront.set(ctre._ctre.ControlMode.PercentOutput, 0.25)
                    self.r_motorFront.set(ctre._ctre.ControlMode.PercentOutput, 0.25)
                else:
                    self.l_motorFront.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
                    self.r_motorFront.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
                    self.autoStage = '3'

            elif self.autoMode == 1 or self.autoMode == 3:
                if r_encoderPos <= 7500:
                    self.l_motorFront.set(ctre._ctre.ControlMode.PercentOutput, 0.25)
                    self.r_motorFront.set(ctre._ctre.ControlMode.PercentOutput, 0.25)
                else:
                    self.l_motorFront.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
                    self.r_motorFront.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
                # ==>> The "if" below will be true in the same case as the "else" above, with the
                # ==>> exception of when r_encoderPos is exactly 7500.  We could put the body of
                # ==>> the "if" into the above "else" with almost the same effect.
                if r_encoderPos >= 7500:
                    motorState = 'on'
                    self.autoStage = '3'

            elif self.autoMode == 2 or self.autoMode == 4:
                # ==>> The logic below could be simplified into the form:
                # ==>> if r_encoderPos <= 7500:
                # ==>>     <drive>
                # ==>> elif r_encoderPos <= 15500:
                # ==>>     <turn>
                # ==>> else:
                # ==>>     <stop and change stage>
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
                    motorState = 'on'
                    self.autoStage = '3'
                    # print (Time)

            # ==>> I think that this whole block from here to my next comment
            # ==>> needs to be unindented one step (4 spaces),
            # ==>> so that it is at the same stage as the "if self.autoStage == '2' above
            # ==>> (or the "elif" if you change it per the comment).  You want it to be
            # ==>> tried when autoStage doesn't equal '1' or '2'.
            # ==>> Also, we would be better off transitioning away from time.sleep() so that
            # ==>> each call of autoPeriodic() can execute quickly.  But I would not suggest
            # ==>> changing it until we get access to the robot again.
            # ==>> Finally, man1_encoder is only obtained once at the top of the function, so
            # ==>> after a time.sleep() the value is stale and doesn't represent the shooter
            # ==>> speed at that moment.  At a minimum, we should get the value again.
            elif self.autoStage == '3':
                if self.autoMode == 0:
                    pass
                if self.autoMode == 1 or self.autoMode == 3:
                    self.man1Shooter.set(ctre._ctre.ControlMode.Velocity, self.targetVelocity)
                    if 11000 <= man1_encoder and man1_encoder <= 11400:

                        if self.autoS1 == 'b':
                            time.sleep(2)
                            self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.85)
                            time.sleep(1.5)
                            self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
                            self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.75)
                            time.sleep(3)
                            self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
                            self.autoS1 = 'f'
                    if 11000 <= man1_encoder and man1_encoder <= 11400:
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
                    if 11000 <= man1_encoder and man1_encoder <= 11400:
                        if self.autoS2 == 'f':
                            time.sleep(1)
                            self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
                            self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.75)
                            time.sleep(1)
                            self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.85)
                # ==>> End of block to be unindented.  That way the "if self.autoMode ==1 ..." block is the same level
                # ==>> as the "if self.autoMode == 2..." below.
                if self.autoMode == 2 or self.autoMode == 4:
                    self.man1Shooter.set(ctre._ctre.ControlMode.Velocity, self.targetVelocity2)
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



        # self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
        #if 11000 <= man1_encoder and man1_encoder <= 11400:
        #    self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.75)
        else:
            self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
            self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.0)


    # D=Drive forward
    """
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


        #if self.ourTimer.hasPeriodPassed(period: seconds) → bool == True:
    def teleopInit(self):
        self.l_motorFront.setSelectedSensorPosition(0)
        self.r_motorFront.setSelectedSensorPosition(0)

    def teleopPeriodic(self):
        
        ColorWheel = getGameSpecificMessage()

        

        
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
            if 11000 <= man1_encoder and man1_encoder <= 11050:
                if self.l_joy.getRawButton(1):
                    self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.75)
                    # self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.55)
                else:
                    self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
                    # self.man1Tread.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
            else:
                self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
        else:
            self.man1Shooter.set(ctre._ctre.ControlMode.PercentOutput, 0.0)
            self.man1Kicker.set(ctre._ctre.ControlMode.PercentOutput, 0.0)


        # This has the color sensor collect color value
        # #This has the color sensor collect color values
        color = self.colorSensor.getColor()
        GameData = str(wpilib.DriverStation.getInstance().getGameSpecificMessage())
        #This has the color sensor collect color values
        color = self.colorSensor.getColor()
        #defines colorstring
        colorstring = 'Unknown'
        colorstring1 = 'Unknown'
        colorstring2 = 'Unknown'
        # resets confidence
        confidence = 0.95
        # uses confidence factor to determine closest color values
        matchedcolor = self.colormatcher.matchClosestColor(color, confidence)
<<<<<<< Updated upstream

        # uses estimated color values to return exact preset colors for printing
        if matchedcolor.red == self.BlueTarget.red and matchedcolor.green == self.BlueTarget.green and matchedcolor.blue == self.BlueTarget.blue:
            colorstring = 'B'


        elif matchedcolor.red == self.RedTarget.red and matchedcolor.green == self.RedTarget.green and matchedcolor.blue == self.RedTarget.blue:
            colorstring = 'R'


        elif matchedcolor.red == self.GreenTarget.red and matchedcolor.green == self.GreenTarget.green and matchedcolor.blue == self.GreenTarget.blue:
            colorstring = 'G'


        elif matchedcolor.red == self.YellowTarget.red and matchedcolor.green == self.YellowTarget.green and matchedcolor.blue == self.YellowTarget.blue:
            colorstring = 'Y'

=======
        
        #uses estimated color values to return exact preset colors for printing
        if matchedcolor.red == self.BlueTarget.red and matchedcolor.green == self.BlueTarget.green and matchedcolor.blue == self.BlueTarget.blue:
            colorstring = 'blue'
        
        elif matchedcolor.red == self.RedTarget.red and matchedcolor.green == self.RedTarget.green and matchedcolor.blue == self.RedTarget.blue:
            colorstring = 'red'
        
        elif matchedcolor.red == self.GreenTarget.red and matchedcolor.green == self.GreenTarget.green and matchedcolor.blue == self.GreenTarget.blue:
            colorstring = 'green'
        elif matchedcolor.red == self.YellowTarget.red and matchedcolor.green == self.YellowTarget.green and matchedcolor.blue == self.YellowTarget.blue:
            colorstring = 'yellow'
            
        
>>>>>>> Stashed changes
        #defines color values
        red = color.red
        blue = color.blue
        green = color.green

        # ==>> As noted above, if we aren't using it, we should delete it.
        # keeps pace and prints results
        self.temp += 1
        if self.temp % 25 == 0:
            print ('{:5.3f} {:5.3f} {:5.3f} {} {} {:5.3f} {:5.3f} {:5.3f} {}'.format(color.red, color.green, color.blue, colorstring, confidence, matchedcolor.red, matchedcolor.green, matchedcolor.blue, GameData))
            print(self.temp)

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


if __name__ == "__main__":
    wpilib.run(MyRobot)


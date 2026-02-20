import wpilib
from crest import Crest

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.crest = Crest()
        self.joystick = wpilib.Joystick(0)

    def teleopPeriodic(self):
        if self.joystick.getRawButton(1):
          self.crest.testeMotor()
        elif self.joystick.getRawButton(2):
          self.crest.Contrario()
        else:
            self.crest.crest_motor.set(0)
        
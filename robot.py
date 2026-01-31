import wpilib
from intake import Intake

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.intake = Intake()
        self.joystick = wpilib.Joystick(0)

    def teleopPeriodic(self):
        if self.joystick.getRawButton(1):
          self.intake.testeMotor()
        elif self.joystick.getRawButton(2):
          self.intake.Contrario()
        else:
            self.intake.arm_motor.set(0)
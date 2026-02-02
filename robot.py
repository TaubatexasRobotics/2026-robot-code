import wpilib
from intake import Intake

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.intake = Intake()
        self.joystick = wpilib.Joystick(0)
    
    def teleopInit(self):
       pass

    def teleopPeriodic(self):
      isEnabled = False
      if self.joystick.getRawButtonPressed(1):
        isEnabled = not isEnabled  

      if isEnabled:
        self.intake.suckBalls()
      else:
        self.intake.stopRoll()

      if self.joystick.getRawButton(2):
         self.intake.turnDown()
      elif self.joystick.getRawButton(3):
         self.intake.turnUp
      else:
         self.intake.stopArm

      


            
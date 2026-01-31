import wpilib
from intake import Intake

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.intake = Intake()
        self.joystick = wpilib.Joystick(0)
    
    def teleopInit(self):
       self.intake.encoder.setPosition(0)

    def teleopPeriodic(self):
        '''
        if self.joystick.getRawButton(1):
          self.intake.testeMotor()
        elif self.joystick.getRawButton(2):
          self.intake.Contrario()
        else:
            self.intake.arm_motor.set(0)
        '''
        if self.joystick.getRawButton(1):
          self.intake.ativar(-0.7)
        elif self.joystick.getRawButton(2):
          self.intake.ativar(0)
        elif self.joystick.getRawButton(3):
          self.intake.arm_motor.set(0.3)
        elif self.joystick.getRawButton(4):
          self.intake.arm_motor.set(-0.3)        
        else:
            self.intake.arm_motor.set(0)
    
    def robotPeriodic(self):
       self.intake.get_posicao_graus()
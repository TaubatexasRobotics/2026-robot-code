import wpilib
from intake import Intake
from drivetrain import Drivetrain

def log_exception(e):
    wpilib.DataLogManager.log(repr(e))
    
class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.intake = Intake()
        self.drivetrain = Drivetrain()
        
        self.joystick = wpilib.Joystick(0)
        self.isIntakeEnabled = False
    
    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        if self.joystick.getRawButtonPressed(1):
            self.isIntakeEnabled = not self.isIntakeEnabled  

        if self.isIntakeEnabled:
            self.intake.suckBalls()
            print("sucking balls")
        else:
            if self.joystick.getRawButton(4):
                self.intake.dropBalls()
                print("drop balls")
            else:
                self.intake.stopRoll()
                print("stop roll")

        if self.joystick.getRawButton(2):
            print("arm down")
            self.intake.turnDown()
        elif self.joystick.getRawButton(3):
            self.intake.turnUp()
            print("arm up")
        else:
            self.intake.stopArm()
            print("arm stopped")

        try:        
            self.drivetrain.arcadeDrive(-self.joystick.getY(), self.joystick.getX())
        except BaseException as e:
            log_exception(e)
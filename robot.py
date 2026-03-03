import wpilib
from intake import Intake
from turret import Turret
from drivetrain import Drivetrain
from commands2 import TimedCommandRobot

def log_exception(e):
    wpilib.DataLogManager.log(repr(e))
    
class MyRobot(TimedCommandRobot):

    def robotInit(self):
        self.intake = Intake()
        self.drivetrain = Drivetrain()
        self.turret = Turret()
        
        self.mechanisms = [self.intake, self.drivetrain, self.turret]
        
        self.joystick = wpilib.Joystick(0)
        self.intake.is_enabled = False
        
        wpilib.SmartDashboard.putNumber("test", 123)
        
    def robotPeriodic(self):
        for mechanism in self.mechanisms:
            try:
                if hasattr(mechanism, "update_dashboard"):
                    mechanism.update_dashboard()
            except BaseException as e:
                log_exception(e)        
    
    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        try:
            self.intake.teleopPeriodic()

        except BaseException as e:
            log_exception(e)

        try:
            self.drivetrain.arcadeDrive(
                self.joystick.getRawAxis(1),
                self.joystick.getRawAxis(0)
            )
        except BaseException as e:
            log_exception(e)
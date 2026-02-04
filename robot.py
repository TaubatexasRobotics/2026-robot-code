import wpilib
from intake import Intake
from turret import Turret
from drivetrain import Drivetrain

def log_exception(e):
    wpilib.DataLogManager.log(repr(e))
    
class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.intake = Intake()
        self.drivetrain = Drivetrain()
        self.turret = Turret()
        
        self.joystick = wpilib.Joystick(0)
        self.is_intake_enabled = False
    
    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        try:
            if self.joystick.getRawButtonPressed(1):
                self.is_intake_enabled = not self.is_intake_enabled  

            if self.is_intake_enabled:
                self.intake.receive()
                print("sucking balls")
            else:
                if self.joystick.getRawButton(4):
                    self.intake.drop()
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

            # if self.joystick.getRawButton(2):
            #     self.turret.shooterSpeed(.8)
            # else:
            #     self.turret.shooterSpeed(0)
                
            # if -0.1 > self.joystick.getRawAxis(4) < 0.1:
            #     self.turret.yaw(0)
            # else:
            #     self.turret.yaw(self.joystick.getRawAxis(4))
        except BaseException as e:
            log_exception(e)

        try:
            self.drivetrain.arcadeDrive(
                self.joystick.getRawAxis(1),
                self.joystick.getRawAxis(0)
            )
        except BaseException as e:
            log_exception(e)
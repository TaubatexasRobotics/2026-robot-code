import wpilib
from drivetrain import Drivetrain
from camera import AprilTagCamera
from turret import Turret
import constants

class Robot(wpilib.TimedRobot):
    def robotInit(self) -> None:
        self.camera = AprilTagCamera(constants.kCameraName)
        self.drivetrain = Drivetrain(AprilTagCamera)
        self.turret = Turret(self.camera)
        self.driver_joystick = wpilib.Joystick(constants.kJoystickDriverPort)
        self.codriver_joystick = wpilib.Joystick(constants.kJoystickCoDriverPort)

    def robotPeriodic(self) -> None:
       # self.drivetrain.updateOdometry()
        pass
    def teleopPeriodic(self) -> None:
        if self.driver_joystick.getRawButton(1):
            self.turret.yawLeft()
        elif self.driver_joystick.getRawButton(3):
            self.turret.yawRight()
        elif self.driver_joystick.getRawButton(2):
            self.turret.TurretAlign(1)
        else:
            self.turret.turnOffKraken()
        self.drivetrain.arcadeDrive(self.driver_joystick.getRawAxis(0),0)

        

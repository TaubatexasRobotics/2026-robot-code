import wpilib
from drivetrain import Drivetrain
from camera import AprilTagCamera
from turret import Turret
import constants

class Robot(wpilib.TimedRobot):
    def robotInit(self) -> None:
        self.camera = AprilTagCamera(constants.kCameraName)
        self.drivetrain = Drivetrain(self.camera)
        self.turret = Turret(self.camera)
        self.driver_joystick = wpilib.Joystick(constants.kJoystickDriverPort)
        self.codriver_joystick = wpilib.Joystick(constants.kJoystickCoDriverPort)

    def robotPeriodic(self) -> None:
        self.drivetrain.updateOdometry()

    def teleopPeriodic(self) -> None:
        if self.joystick.getRawButton(1):
            self.turret.yawLeft()
        elif self.joystick.getRawButton(3):
            self.turret.yawRight()
        elif self.joystick.getRawButton(2):
            self.turret.TurretAlign(1)
        else:
            self.turret.turnOffKraken()

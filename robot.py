from wpilib import TimedRobot
from drivetrain import Drivetrain
from camera import AprilTagCamera
from turret import Turret
from genericjoystick import GenericJoystick
import constants

class Robot(TimedRobot):
    def robotInit(self) -> None:
        self.camera = AprilTagCamera(constants.kCameraName)
        self.drivetrain = Drivetrain(self.camera)
        self.turret = Turret(self.camera)
        self.driver_joystick = GenericJoystick(constants.kJoystickDriverPort)
        self.codriver_joystick = GenericJoystick(constants.kJoystickCoDriverPort)

    def robotPeriodic(self) -> None:
        self.drivetrain.updateOdometry()

    def teleopPeriodic(self) -> None:
        if self.joystick.getA():
            self.turret.yawLeft()
        elif self.joystick.getB():
            self.turret.yawRight()
        elif self.joystick.getC():
            self.turret.TurretAlign(1)
        else:
            self.turret.turnOffKraken()

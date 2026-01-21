from wpilib import TimedRobot, Joystick
from drivetrain import Drivetrain
from camera import AprilTagCamera
from genericjoystick import GenericJoystick

class Robot(TimedRobot):
    def robotInit(self) -> None:
        self.drivetrain = Drivetrain()
        self.joystick = Joystick(0)
        print("saddsadasdasd", self.joystick.getName())

    def teleopPeriodic(self) -> None:
        self.drivetrain.arcadeDriveAimAndRange(3)
    
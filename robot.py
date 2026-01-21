from wpilib import TimedRobot
from drivetrain import Drivetrain
from camera import AprilTagCamera

class Robot(TimedRobot):
    def robotInit(self) -> None:
        self.drivetrain = Drivetrain()
    
    def teleopPeriodic(self) -> None:
        self.drivetrain.arcadeDriveAimAndRange(3)
        self.drivetrain.distance
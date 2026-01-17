from wpilib import TimedRobot
from drivetrain import Drivetrain
from camera import AprilTagCamera

class Robot(TimedRobot):
    def robotInit(self) -> None:
        self.drivetrain = Drivetrain()
        

    def teleopInit(self) -> None:
        pass
    
    def teleopPeriodic(self) -> None:
        self.drivetrain.arcadeDriveAlign(3)
        self.drivetrain.arcadeDriveAlign2

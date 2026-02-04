from wpilib import TimedRobot
from limelight_camera import LimeLightCamera

class Robot(TimedRobot):
    def robotInit(self) -> None:
        self.camera = LimeLightCamera()

    def robotPeriodic(self) -> None:
        self.camera.logging()

    def teleopPeriodic(self) -> None:
        pass
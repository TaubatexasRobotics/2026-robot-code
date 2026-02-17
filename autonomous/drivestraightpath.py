from commands2 import WaitCommand
from drivetrain import Drivetrain
from wpimath import units


class DriveStraightPath(WaitCommand):
    def __init__(
        self, drivetrain: Drivetrain, seconds: units.seconds, backward: bool = False
    ) -> None:
        super().__init__(seconds)
        self.drivetrain = drivetrain
        self.backwards = backward

        self.addRequirements(drivetrain)

    def initialize(self) -> None:
        self.drivetrain.stop()

    def execute(self) -> None:
        if self.backward:
            self.drivetrain.backward()
        else:
            self.drivetrain.forward()

    def end(self, interrupted: bool) -> None:
        self.drivetrain.stop()

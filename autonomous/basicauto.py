import constants
from commands2 import Command
from wpimath.controller import LTVUnicycleController
from drivetrain import Drivetrain
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator
from wpimath.geometry import Pose2d, Rotation2d, Translation2d


class BasicAuto(Command):
    def __init__(self, drivetrain: Drivetrain) -> None:
        super().__init__()
        self.trajectory = TrajectoryGenerator.generateTrajectory(
           Pose2d(0, 0, Rotation2d(0)), 
           [Translation2d(1, 1), Translation2d(2, -1)],
           Pose2d(3, 0, Rotation2d(0)), 
           TrajectoryConfig(0.5, 0.5)
        )
        self.reference = self.trajectory.sample(3)
        self.controller = LTVUnicycleController(0.020)

        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)

    def execute(self) -> None:
        adjustedSpeeds = self.controller.calculate(
            self.drivetrain.getPose(), self.reference
        )

        wheelSpeeds = constants.kDrivetrainKinematics.toWheelSpeeds(adjustedSpeeds)

        self.drivetrain.driveWithWheelSpeeds(wheelSpeeds)

    def end(self, interrupted: bool) -> None:
        self.drivetrain.stop()

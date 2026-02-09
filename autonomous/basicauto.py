import constants
from commands2 import Command
from wpimath.controller import (
    LTVUnicycleController,
    SimpleMotorFeedforwardMeters,
)
from drivetrain import Drivetrain
from wpimath.trajectory.constraint import DifferentialDriveVoltageConstraint
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator
from wpimath.geometry import Pose2d, Rotation2d, Translation2d

class BasicAuto(Command):
    def __init__(self, drivetrain: Drivetrain) -> None:
        super().__init__()

        self.feedforward = SimpleMotorFeedforwardMeters(
            constants.ksVolts,
            constants.kvVoltSecondsPerMeter,
            constants.kaVoltSecondsSquaredPerMeter,
        )

        autoVoltageConstraint = DifferentialDriveVoltageConstraint(
            self.feedforward,
            constants.kDrivetrainKinematics,
            maxVoltage=10,  # 10 volts max.
        )

        # Create config for trajectory
        config = TrajectoryConfig(
            constants.kMaxVelocityMetersPerSecond,
            constants.kMaxAccelerationMetersPerSecondSquared,
        )
        # Add kinematics to ensure max speed is actually obeyed
        config.setKinematics(constants.kDrivetrainKinematics)
        # Apply the voltage constraint
        config.addConstraint(autoVoltageConstraint)
        
        self.trajectory = TrajectoryGenerator.generateTrajectory(
            # Start at the origin facing the +x direction.
            Pose2d(0, 0, Rotation2d(0)),
            # Pass through these two interior waypoints, making an 's' curve path
            [Translation2d(1, 1), Translation2d(2, -1)],
            # End 3 meters straight ahead of where we started, facing forward
            Pose2d(3, 0, Rotation2d(0)),
            # Pass config
            config,
        )

        self.controller = LTVUnicycleController([0.0625, 0.125, 2.0], [1.0, 2.0], 0.02, 9)

        self.drivetrain = drivetrain
        self.reference = self.trajectory.sample(3.4)
        self.addRequirements(drivetrain)

    def execute(self) -> None:
        adjustedSpeeds = self.controller.calculate(
            self.drivetrain.getPose(),
            self.reference
        )

        wheelSpeeds = constants.kDrivetrainKinematics.toWheelSpeeds(adjustedSpeeds)

        left_volts = self.feedforward.calculate(wheelSpeeds.left)
        right_volts = self.feedforward.calculate(wheelSpeeds.right)           

        self.drivetrain.tankDriveVolts(left_volts, right_volts)
    
    def end(self, interrupted: bool) -> None:
        self.drivetrain.stop()
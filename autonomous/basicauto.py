import constants
from commands2 import RamseteCommand
from wpimath.controller import (
    RamseteController,
    PIDController,
    SimpleMotorFeedforwardMeters,
)
from drivetrain import Drivetrain
from wpimath.trajectory.constraint import DifferentialDriveVoltageConstraint
from wpimath.trajectory import TrajectoryConfig, TrajectoryGenerator
from wpimath.geometry import Pose2d, Rotation2d, Translation2d

class BasicAuto(RamseteCommand):
    def __init__(self, drivetrain: Drivetrain) -> None:
        autoVoltageConstraint = DifferentialDriveVoltageConstraint(
            SimpleMotorFeedforwardMeters(
                constants.ksVolts,
                constants.kvVoltSecondsPerMeter,
                constants.kaVoltSecondsSquaredPerMeter,
            ),
            constants.kDriveKinematics,
            maxVoltage=10,  # 10 volts max.
        )

        # Create config for trajectory
        config = TrajectoryConfig(
            constants.kMaxVelocityMetersPerSecond,
            constants.kMaxAccelerationMetersPerSecondSquared,
        )
        # Add kinematics to ensure max speed is actually obeyed
        config.setKinematics(constants.kDriveKinematics)
        # Apply the voltage constraint
        config.addConstraint(autoVoltageConstraint)
        
        self.exampleTrajectory = TrajectoryGenerator.generateTrajectory(
            # Start at the origin facing the +x direction.
            Pose2d(0, 0, Rotation2d(0)),
            # Pass through these two interior waypoints, making an 's' curve path
            [Translation2d(1, 1), Translation2d(2, -1)],
            # End 3 meters straight ahead of where we started, facing forward
            Pose2d(3, 0, Rotation2d(0)),
            # Pass config
            config,
        )

        self.drivetrain = drivetrain

        super().__init__(
            self.exampleTrajectory,
            self.drivetrain.getPose,
            RamseteController(constants.kRamseteB, constants.kRamseteZeta),
            SimpleMotorFeedforwardMeters(
                constants.ksVolts,
                constants.kvVoltSecondsPerMeter,
                constants.kaVoltSecondsSquaredPerMeter,
            ),
            constants.kDriveKinematics,
            self.drivetrain.getWheelSpeeds,
            PIDController(*constants.kDrivetrainPID),
            PIDController(*constants.kDrivetrainPID),
            # RamseteCommand passes volts to the callback
            self.drivetrain.tankDriveVolts,
            [self.drivetrain],
        )
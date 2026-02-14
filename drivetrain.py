import constants
from commands2 import Subsystem, Command
from typing import Optional
from camera import Camera
from wpilib import DriverStation, Field2d, SmartDashboard
from navx import AHRS
from wpilib.drive import DifferentialDrive
from wpimath.controller import PIDController, SimpleMotorFeedforwardMeters
from wpimath.kinematics import (
    DifferentialDriveOdometry, 
    DifferentialDriveWheelSpeeds, 
    ChassisSpeeds,
)
from wpimath.geometry import Pose2d, Rotation2d
from rev import (
    SparkMax,
    SparkMaxConfig,
    ResetMode,
    PersistMode,
    SparkLowLevel,
    ClosedLoopSlot,
)
from wpilib.simulation import DifferentialDrivetrainSim
from wpimath.system.plant import LinearSystemId, DCMotor
from pathplannerlib.auto import AutoBuilder
from pathplannerlib.controller import PPLTVController
from pathplannerlib.config import RobotConfig

class Drivetrain(Subsystem):
    def __init__(self) -> None:
        self.left_front_motor = SparkMax(
            constants.kLeftFrontId, constants.kDrivetrainMotorType
        )
        self.left_back_motor = SparkMax(
            constants.kLeftBackId, constants.kDrivetrainMotorType
        )
        self.right_front_motor = SparkMax(
            constants.kRightFrontId, constants.kDrivetrainMotorType
        )
        self.right_back_motor = SparkMax(
            constants.kRightBackId, constants.kDrivetrainMotorType
        )

        self.drivetrain = DifferentialDrive(
            self.left_front_motor, self.right_front_motor
        )
        self.drivetrain.setSafetyEnabled(True)
        self.field = Field2d()

        """
        self.drivetrain_system = LinearSystemId.identifyDrivetrainSystem(1.98, 0.2, 1.5, 0.3)
        self.drivetrain_simulator = DifferentialDrivetrainSim(
            self.drivetrain_system,
            DCMotor.NEO(4),
            8,
            constants.kTrackWidth,
            constants.kWheelDiameter / 2,
            None
        )
        """

        config = SparkMaxConfig()

        config.smartCurrentLimit(constants.kDrivetrainSmartCurrentLimit)
        config.setIdleMode(constants.kDrivetrainIdleMode)
        config.closedLoop.pid(*constants.kDrivetrainPID)
        config.closedLoop.velocityFF(constants.kvVoltSecondsPerMeter)
        config.closedLoop.maxMotion.maxAcceleration(
            constants.kMaxAccelerationMetersPerSecondSquared
        )
        config.closedLoop.maxMotion.maxVelocity(constants.kMaxVelocityMetersPerSecond)
        config.closedLoop.setFeedbackSensor(constants.kFeedbackSensor)

        config.encoder.positionConversionFactor(constants.kRotationsToMeters)
        config.encoder.velocityConversionFactor(
            constants.kRotationsPerMinuteToMetersPerSecond
        )
        config.inverted(constants.kLeftMotorsInverted)

        self.left_front_motor.configure(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )

        config.follow(constants.kLeftFrontId)
        self.left_back_motor.configure(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )

        config.disableFollowerMode()
        config.inverted(constants.kRightMotorsInverted)

        self.right_front_motor.configure(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )
        config.follow(constants.kRightFrontId)
        self.right_back_motor.configure(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )

        config.disableFollowerMode()

        self.left_encoder = self.left_front_motor.getEncoder()
        self.right_encoder = self.right_front_motor.getEncoder()

        self.left_closed_loop = self.left_front_motor.getClosedLoopController()
        self.right_closed_loop = self.right_front_motor.getClosedLoopController()

        self.left_encoder.setPosition(0)
        self.right_encoder.setPosition(0)

        self.navx = AHRS.create_spi()
        self.navx.reset()

        self.pid_angular = PIDController(*constants.kDrivetrainPID)
        self.pid_forward = PIDController(*constants.kDrivetrainPID)

        rotation = Rotation2d.fromDegrees(self.navx.getAngle())

        self.odometry = DifferentialDriveOdometry(
            rotation,
            self.left_encoder.getPosition(),
            self.right_encoder.getPosition(),
            Pose2d(*constants.kInitialPose),
        )

        self.feedforward = SimpleMotorFeedforwardMeters(
            constants.ksVolts,
            constants.kvVoltSecondsPerMeter,
            constants.kaVoltSecondsSquaredPerMeter,
        )

        try:
            pathConfig = RobotConfig.fromGUISettings()
        except:
            raise Exception("ERROR: No Robot Config Loaded.")

        AutoBuilder.configure(
            self.getPose,
            self.resetPose,
            self.getRelativeSpeeds,
            lambda speeds, feedforwards: self.driveRobotRelative(speeds),
            PPLTVController(0.02),
            pathConfig,
            self.shouldFlipPath,
            self
        )
    
    def stop(self) -> None:
        self.drivetrain.arcadeDrive(0, 0)

    def resetEncoders(self) -> None:
        self.left_encoder.setPosition(0)
        self.right_encoder.setPosition(0)

    def shouldFlipPath(self) -> None:
        return DriverStation.getAlliance() == DriverStation.Alliance.kRed

    def resetPose(self, pose: Pose2d) -> None:
        self.odometry.resetPosition(
            Rotation2d.fromDegrees(self.navx.getAngle()),
            self.left_encoder.getPosition(),
            self.right_encoder.getPosition(),
            pose,
        )

    def getPose(self) -> Pose2d:
        return self.odometry.getPose()

    def setSpeeds(self, speeds: DifferentialDriveWheelSpeeds) -> None:
        left_feedforward = self.feedforward.calculate(speeds.left)
        right_feedforward = self.feedforward.calculate(speeds.right)

        self.left_closed_loop.setReference(
            speeds.left,
            SparkLowLevel.ControlType.kVelocity,
            ClosedLoopSlot.kSlot0,
            left_feedforward,
        )
        self.right_closed_loop.setReference(
            speeds.right,
            SparkLowLevel.ControlType.kVelocity,
            ClosedLoopSlot.kSlot0,
            right_feedforward,
        )

    def getWheelSpeeds(self) -> DifferentialDriveWheelSpeeds:
        return DifferentialDriveWheelSpeeds(
            self.left_encoder.getVelocity(), self.right_encoder.getVelocity()
        )

    def getRelativeSpeeds(self) -> ChassisSpeeds:
        return constants.kDriveKinematics.toChassisSpeeds(
            DifferentialDriveWheelSpeeds(
                self.left_encoder.getVelocity(), self.right_encoder.getVelocity()
            )
        )
    
    def forward(self) -> Command:
        self.run(lambda: self.drivetrain.arcadeDrive(1, 0))

    def backward(self) -> None:
        self.run(lambda: self.drivetrain.arcadeDrive(-1, 0))

    def arcadeDrive(self, speed: float, rotate: float) -> Command:
        self.run(lambda: self.drivetrain.arcadeDrive(speed, rotate))

    def cheesyDrive(self, speed: float, rotate: float) -> Command:
        self.run(lambda: self.drivetrain.curvatureDrive(speed, rotate))

    def tankDrive(self, left_speed: float, right_speed: float) -> Command:
        self.run(lambda: self.drivetrain.tankDrive(left_speed, right_speed))

    def periodic(self) -> None:
        self.field.setRobotPose(self.odometry.getPose())
        SmartDashboard.putData("Field", self.field)
        self.odometry.update(
            Rotation2d.fromDegrees(self.navx.getAngle()),
            self.left_encoder.getPosition(),
            self.right_encoder.getPosition(),
        )

    def arcadeDriveAlign(self, camera: Camera, tag: int) -> None:
        yaw = camera.getYaw(tag)
        turn = self.pid_angular.calculate(yaw, 0) if yaw != -1 else 0
        self.drivetrain.arcadeDrive(0, turn)

    def arcadeDriveAimAndRange(self, camera: Camera, tag: int) -> None:
        yaw, range = camera.getYawWithRange(tag)
        range = (
            self.pid_forward.calculate(range, constants.kGoalRangeMeters)
            if yaw != -1
            else 0
        )
        rotation = self.pid_angular.calculate(yaw, 0) if yaw != -1 else 0
        self.drivetrain.arcadeDrive(range, rotation)

    def zRotationFromDegrees(self, setpoint: Optional[float]) -> None:
        self.pid_angular.setSetpoint(setpoint)
        self.drivetrain.arcadeDrive(
            0,
            self.pid_angular.calculate(
                self.navx.getAngle(), self.pid_angular.getSetpoint()
            ),
        )

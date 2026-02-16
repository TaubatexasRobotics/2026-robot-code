import constants
from commands2 import Subsystem, Command
from typing import Callable
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
from pathplannerlib.auto import AutoBuilder
from pathplannerlib.controller import PPLTVController
from pathplannerlib.config import RobotConfig
from commands2.sysid import SysIdRoutine
from wpimath.units import volts
from wpilib import RobotController
from wpilib.sysid import SysIdRoutineLog
from math import pi


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
        self.drivetrain.setExpiration(0.1)
        self.drivetrain.setMaxOutput(1.0)

        self.field = Field2d()

        config = SparkMaxConfig()

        config.smartCurrentLimit(constants.kDrivetrainSmartCurrentLimit)
        config.setIdleMode(constants.kDrivetrainIdleMode)
        config.closedLoop.pid(*constants.kDrivetrainPID)
        config.closedLoop.feedForward.sva(*constants.kDrivetrainFeedForward)
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

        self.pid_forward = PIDController(*constants.kDrivetrainPID[:3])
        self.pid_angular = PIDController(*constants.kDrivetrainPID[:3])

        self.pid_angular.enableContinuousInput(-pi, pi)

        self.odometry = DifferentialDriveOdometry(
            Rotation2d.fromDegrees(self.navx.getAngle()),
            self.left_encoder.getPosition(),
            self.right_encoder.getPosition(),
            Pose2d(*constants.kInitialPose),
        )

        try:
            pathConfig = RobotConfig.fromGUISettings()
        except:
            raise Exception("ERROR: No Robot Config Loaded.")

        AutoBuilder.configure(
            self.getPose,
            self.resetPose,
            self.getRelativeSpeeds,
            lambda speeds, feedforwards: self.driveWithRelativeSpeeds(speeds),
            PPLTVController(0.02),
            pathConfig,
            self.shouldFlipPath,
            self
        )

        self.sys_id_routine = SysIdRoutine(
            SysIdRoutine.Config(),
            SysIdRoutine.Mechanism(self.sysIdDriveVoltage, self.log, self),
        )

            
    def stop(self) -> None:
        self.drivetrain.arcadeDrive(0, 0)

    def resetEncoders(self) -> None:
        self.left_encoder.setPosition(0)
        self.right_encoder.setPosition(0)

    def shouldFlipPath(self) -> bool:
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

    def driveWithWheelSpeeds(self, speeds: DifferentialDriveWheelSpeeds, feedforward: SimpleMotorFeedforwardMeters) -> None:
        left_feedforward = feedforward.calculate(speeds.left)
        right_feedforward = feedforward.calculate(speeds.right)

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
    
    def driveWithRelativeSpeeds(self, chassisSpeeds: ChassisSpeeds) -> None:
        wheelSpeeds = constants.kDrivetrainKinematics.toWheelSpeeds(chassisSpeeds)
        self.left_closed_loop.setSetpoint(
            wheelSpeeds.left, SparkLowLevel.ControlType.kVelocity
        )
        self.right_closed_loop.setSetpoint(
            wheelSpeeds.right, SparkLowLevel.ControlType.kVelocity
        )

    def getWheelSpeeds(self) -> DifferentialDriveWheelSpeeds:
        return DifferentialDriveWheelSpeeds(
            self.left_encoder.getVelocity(), self.right_encoder.getVelocity()
        )

    def getRelativeSpeeds(self) -> ChassisSpeeds:
        return constants.kDrivetrainKinematics.toChassisSpeeds(
            DifferentialDriveWheelSpeeds(
                self.left_encoder.getVelocity(), self.right_encoder.getVelocity()
            )
        )
    
    def forward(self) -> Command:
        return self.run(lambda: self.drivetrain.arcadeDrive(1, 0))

    def backward(self) -> Command:
        return self.run(lambda: self.drivetrain.arcadeDrive(-1, 0))

    def arcadeDrive(self, speed: Callable[[], float], rotate: Callable[[], float]) -> Command:
        return self.run(lambda: self.drivetrain.arcadeDrive(speed(), rotate()))

    def cheesyDrive(self, speed: Callable[[], float], rotate: Callable[[], float], allowTurnInPlace: bool) -> Command:
        return self.run(lambda: self.drivetrain.curvatureDrive(speed(), rotate(), allowTurnInPlace))

    def tankDrive(self, left_speed: Callable[[], float], right_speed: Callable[[], float]) -> Command:
        return self.run(lambda: self.drivetrain.tankDrive(left_speed(), right_speed()))
    
    def sysIdDriveVoltage(self, voltage: volts) -> None:
        self.left_front_motor.setVoltage(voltage)
        self.right_front_motor.setVoltage(voltage)

    def log(self, sys_id_routine: SysIdRoutineLog) -> None:
        sys_id_routine.motor("drive-left").voltage(
            self.left_front_motor.get() * RobotController.getBatteryVoltage()
        ).position(self.left_encoder.getPosition()).velocity(
            self.left_encoder.getVelocity()
        )

        sys_id_routine.motor("drive-right").voltage(
            self.right_front_motor.get() * RobotController.getBatteryVoltage()
        ).position(self.right_encoder.getPosition()).velocity(
            self.right_encoder.getVelocity()
        )

    def sysIdQuasistatic(self, direction: SysIdRoutine.Direction) -> Command:
        return self.sys_id_routine.quasistatic(direction)

    def sysIdDynamic(self, direction: SysIdRoutine.Direction) -> Command:
        return self.sys_id_routine.dynamic(direction)

    def periodic(self) -> None:
        self.field.setRobotPose(self.odometry.getPose())
        SmartDashboard.putData("Field", self.field)
        self.odometry.update(
            Rotation2d.fromDegrees(self.navx.getAngle()),
            self.left_encoder.getPosition(),
            self.right_encoder.getPosition(),
        )

    def aim(self, camera: Camera, tag: int) -> None:
        yaw = camera.getYawFromTag(tag)
        turn = self.pid_angular.calculate(yaw, 0) if yaw != -1 else 0
        self.drivetrain.arcadeDrive(0, turn)

    def aimAndRange(self, camera: Camera, tag: int) -> None:
        yaw, range = camera.getYawAndRangeFromTag(tag)
        range = (
            self.pid_forward.calculate(range, constants.kGoalRangeMeters)
            if yaw != -1
            else 0
        )
        rotation = self.pid_angular.calculate(yaw, 0) if yaw != -1 else 0
        self.drivetrain.arcadeDrive(range, rotation)

    def rotate(self, angle: float) -> None:
        self.pid_angular.setSetpoint(angle)
        self.drivetrain.arcadeDrive(
            0,
            self.pid_angular.calculate(
                self.navx.getAngle(), self.pid_angular.getSetpoint()
            ),
        )

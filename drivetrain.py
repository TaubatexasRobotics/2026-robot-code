import constants
from commands2 import Subsystem
from typing import Optional
from photonvisioncamera import PhotonVisionCamera
from wpilib import MotorControllerGroup, DriverStation
from navx import AHRS
from wpilib.drive import DifferentialDrive
from wpimath.controller import PIDController
from wpimath.kinematics import DifferentialDriveOdometry, DifferentialDriveWheelSpeeds
from wpimath.geometry import Pose2d, Rotation2d
from rev import SparkMax, SparkMaxConfig, ResetMode, PersistMode

class Drivetrain(Subsystem):
    def __init__(self, camera: PhotonVisionCamera) -> None:
        self.left_front_motor = SparkMax(constants.kLeftFrontId, constants.kDrivetrainMotorType)
        self.left_back_motor = SparkMax(constants.kLeftBackId, constants.kDrivetrainMotorType)
        self.right_front_motor = SparkMax(constants.kRightFrontId, constants.kDrivetrainMotorType)
        self.right_back_motor = SparkMax(constants.kRightBackId, constants.kDrivetrainMotorType)

        self.left_motors = MotorControllerGroup(self.left_front_motor, self.left_back_motor)
        self.right_motors = MotorControllerGroup(self.right_front_motor, self.right_back_motor)
        self.left_motors.setInverted(constants.kLeftMotorsInverted)
        self.right_motors.setInverted(constants.kRightMotorsInverted)
        self.drivetrain = DifferentialDrive(self.left_motors, self.right_motors)

        config = SparkMaxConfig()

        config.smartCurrentLimit(constants.kDrivetrainSmartCurrentLimit)
        config.setIdleMode(constants.kDrivetrainIdleMode)
        config.closedLoop.pid(*constants.kDrivetrainPID)
        config.closedLoop.velocityFF(constants.kvVoltSecondsPerMeter)
        config.closedLoop.maxMotion.maxAcceleration(constants.kMaxAccelerationMetersPerSecondSquared)
        config.closedLoop.maxMotion.maxVelocity(constants.kMaxVelocityMetersPerSecond)

        config.encoder.positionConversionFactor(constants.kRotationsToMeters)
        config.encoder.velocityConversionFactor(constants.kRotationsPerMinuteToMetersPerSecond)
        config.inverted(constants.kLeftMotorsInverted)

        self.left_front_motor.configure(config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters)
        self.left_back_motor.configure(config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters)
        
        config.inverted(constants.kRightMotorsInverted)
        
        self.right_front_motor.configure(config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters)
        self.right_back_motor.configure(config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters)

        self.left_encoder = self.left_front_motor.getEncoder()
        self.right_encoder = self.right_front_motor.getEncoder()

        self.left_encoder.setPosition(0)
        self.right_encoder.setPosition(0)

        self.navx = AHRS.create_spi()
        self.navx.reset()

        self.pid_angular = PIDController(*constants.kDrivetrainPID)
        self.pid_forward = PIDController(*constants.kDrivetrainPID)

        rotation = Rotation2d.fromDegrees(self.navx.getAngle())

        self.pose = Pose2d(*constants.kInitialPose)

        self.odometry = DifferentialDriveOdometry(
            rotation, 
            self.left_encoder.getPosition(), 
            self.right_encoder.getPosition(), 
            self.pose
        )

        self.camera = camera

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
            pose
        )
    
    def getPose(self) -> Pose2d:
        return self.odometry.getPose()

    def tankDriveVolts(self, left_volts: float, right_volts: float) -> None:
        """Controls the left and right sides of the drive directly with voltages."""
        self.left_motors.setVoltage(left_volts)
        self.right_motors.setVoltage(right_volts)
        self.drivetrain.feed()
    
    def getWheelSpeeds(self) -> None:
        return DifferentialDriveWheelSpeeds(
            self.left_encoder.getVelocity(),
            self.right_encoder.getVelocity()
        )

    def front(self) -> None:
        self.drivetrain.arcadeDrive(1, 0)

    def back(self) -> None:
        self.drivetrain.arcadeDrive(-1, 0)

    def arcadeDrive(self, speed: float, rotate: float) -> None:
        self.drivetrain.arcadeDrive(speed, rotate)

    def cheesyDrive(self, speed: float, rotate: float) -> None:
        self.drivetrain.curvatureDrive(speed, rotate)

    def tankDrive(self, left_speed: float, right_speed: float) -> None:
        self.drivetrain.tankDrive(left_speed, right_speed)

    def periodic(self) -> None:
        self.odometry.update(
            Rotation2d.fromDegrees(self.navx.getAngle()),
            self.left_encoder.getPosition(),
            self.right_encoder.getPosition(),
        )

    def arcadeDriveAlign(self, tag: int) -> None:
        yaw = self.camera.getYaw(tag)
        turn = self.pid_angular.calculate(yaw, 0) if yaw != -1 else 0
        self.drivetrain.arcadeDrive(0, turn)
    
    def arcadeDriveAimAndRange(self, tag: int) -> None:
        yaw, range = self.camera.getYawWithRange(tag)
        range = self.pid_forward.calculate(range, constants.kGoalRangeMeters) if yaw != -1 else 0
        rotation = self.pid_angular.calculate(yaw, 0) if yaw != -1 else 0
        self.drivetrain.arcadeDrive(range, rotation)
    
    def zRotationFromDegrees(self, setpoint: Optional[float]) -> None:
        self.pid_angular.setSetpoint(setpoint)
        self.drivetrain.arcadeDrive(0, self.pid_angular.calculate(self.navx.getAngle(), self.pid_angular.getSetpoint()))
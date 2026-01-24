from logging import config
import constants

from commands2 import Subsystem
from typing import Optional
from camera import AprilTagCamera
from phoenix5 import WPI_VictorSPX
from wpilib import MotorControllerGroup, DriverStation, Encoder
from navx import AHRS
from wpilib.drive import DifferentialDrive
from wpimath.controller import PIDController
from wpimath.geometry import Pose2d, Rotation2d
from pathplannerlib.auto import AutoBuilder
from pathplannerlib.controller import PPLTVController
from pathplannerlib.config import RobotConfig
from wpimath.kinematics import DifferentialDriveOdometry, ChassisSpeeds, DifferentialDriveWheelSpeeds, DifferentialDriveKinematics
from wpimath.units import inchesToMeters
import rev

class Drivetrain(Subsystem):
    def __init__(self, camera: AprilTagCamera) -> None:
        self.left_front_motor = rev.SparkMax(constants.kLeftFrontId, rev.SparkLowLevel.MotorType.kBrushless)
        self.left_back_motor = rev.SparkMax(constants.kLeftBackId, rev.SparkLowLevel.MotorType.kBrushless)
        self.right_front_motor = rev.SparkMax(constants.kRightFrontId, rev.SparkLowLevel.MotorType.kBrushless)
        self.right_back_motor = rev.SparkMax(constants.kRightBackId, rev.SparkLowLevel.MotorType.kBrushless)

        self.left_motors = MotorControllerGroup(self.left_front_motor, self.left_back_motor)
        self.right_motors = MotorControllerGroup(self.right_front_motor, self.right_back_motor)
        self.right_motors.setInverted(True)
        self.drivetrain = DifferentialDrive(self.left_motors, self.right_motors)

        config = rev.SparkMaxConfig()
        config.closedLoop.setFeedbackSensor(rev.FeedbackSensor.kPrimaryEncoder)
        config.closedLoop.pid(0.00005,0,0)
        config.closedLoop.velocityFF(0.15)

        config.encoder.positionConversionFactor(constants.kWheelCircunference / constants.kGearReduction)

        self.left_front_motor.configure(config, rev.ResetMode.kResetSafeParameters, rev.PersistMode.kPersistParameters)
        self.left_back_motor.configure(config, rev.ResetMode.kResetSafeParameters, rev.PersistMode.kPersistParameters)
        self.right_front_motor.configure(config, rev.ResetMode.kResetSafeParameters, rev.PersistMode.kPersistParameters)
        self.right_back_motor.configure(config, rev.ResetMode.kResetSafeParameters, rev.PersistMode.kPersistParameters)   

        self.rightClosedLoop = self.right_front_motor.getClosedLoopController()
        self.right2ClosedLoop = self.right_back_motor.getClosedLoopController()
        self.leftClosedLoop = self.left_front_motor.getClosedLoopController()
        self.left2ClosedLoop = self.left_back_motor.getClosedLoopController()


        self.left_encoder = self.left_front_motor.getEncoder()
        self.right_encoder = self.right_front_motor.getEncoder()

        self.left_encoder.setPosition(0)
        self.right_encoder.setPosition(0)



        self.navx = AHRS.create_spi()
        self.navx.reset()

        self.pid_angular = PIDController(*constants.kPIDAngularDrivetrain)
        self.pid_forward = PIDController(*constants.kPIDForwardDrivetrain)

        rotation = Rotation2d.fromDegrees(self.navx.getAngle())

        pathConfig = RobotConfig.fromGUISettings()

        self.pose = Pose2d(*constants.kInitialPose)

        self.odometry = DifferentialDriveOdometry(
            rotation, 
            self.left_encoder.getPosition(), 
            self.right_encoder.getPosition(), 
            self.pose
        )

        self.kinematics = DifferentialDriveKinematics(
            constants.kTrackWidthInMeters
        )

        AutoBuilder.configure (
            self.odometry.getPose,
            self.resetPose,
            self.getRobotRelativeSpeeds,
            lambda speeds, feedforwards: self.driveRobotRelative(speeds),
            PPLTVController(0.02),
            pathConfig,
            self.shouldFlipPath,
            self
        )

        self.camera = camera

    def shouldFlipPath():
        return DriverStation.getAlliance() == DriverStation.Alliance.kRed

    def resetPose(self, pose: Pose2d) -> None:
        self.odometry.resetPosition(
            Rotation2d.fromDegrees(self.navx.getAngle()),
            self.left_encoder.getPosition,
            self.right_encoder.getPosition(),
            pose
        )

    def driveRobotRelative(self, chassiSpeed):
        wheelSpeeds = self.kinematics.toWheelSpeeds(chassiSpeed)
        
        leftRpm = (wheelSpeeds.left / constants.kWheelCircunference) * 60
        rightRpm = (wheelSpeeds.right / constants.kWheelCircunference) * 60

        leftMotorRpm = leftRpm * constants.kGearReduction
        rightMotorRpm = rightRpm * constants.kGearReduction

        self.leftClosedLoop.setReference(leftMotorRpm, rev.SparkBase.ControlType.kVelocity)
        self.left2ClosedLoop.setReference(leftMotorRpm, rev.SparkBase.ControlType.kVelocity)
        self.rightClosedLoop.setReference(rightMotorRpm, rev.SparkBase.ControlType.kVelocity)
        self.right2ClosedLoop.setReference(rightMotorRpm, rev.SparkBase.ControlType.kVelocity)

    def getRobotRelativeSpeeds(self) -> ChassisSpeeds:
        wheelSpeeds = DifferentialDriveWheelSpeeds(
            self.left_encoder.getVelocity(),
            self.right_encoder.getVelocity()
        )

        return self.kinematics.toChassisSpeeds(wheelSpeeds)
    
    def front(self) -> None:
        self.drivetrain.tankDrive(1, 0)

    def back(self) -> None:
        self.drivetrain.tankDrive(-1, 0)

    def arcadeDrive(self, speed: float, rotate: float) -> None:
        self.drivetrain.arcadeDrive(speed, rotate)

    def tankDrive(self, left_speed: float, right_speed: float) -> None:
        self.drivetrain.tankDrive(left_speed, right_speed)

    def updateOdometry(self):
        """Updates the field-relative position."""
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
        rotation = self.pid_angular.calculate(yaw, 0)
        self.drivetrain.arcadeDrive(range, rotation)
    
    def turnToDegrees(self, setpoint: Optional[int]) -> None:
        self.drivetrain.arcadeDrive(0, self.pid_angular.calculate(self.navx.getAngle(), self.pid_angular.getSetpoint()))

    def turnTo90DegreesPositive(self, setpoint: Optional[int]) -> None:
        if (self.navx.getYaw > 90):
            setpoint = self.navx.getYaw - 270 / 360
        else:
            setpoint = self.navx.getYaw + 90 / 360        

        self.drivetrain.arcadeDrive(0, self.pid_angular.calculate(self.navx.getAngle(), setpoint))

    def turnTo90DegreesNegative(self, setpoint: Optional[int]) -> None:
        if (self.navx.getYaw < -90):
            setpoint = self.navx.getYaw + 270 / 360
        else:
            setpoint = self.navx.getYaw - 90          

        self.drivetrain.arcadeDrive(0, self.pid_angular.calculate(self.navx.getAngle(), -setpoint))

    def turnTo180Degrees(self, setpoint: Optional[int]) -> None:
        setpoint = 180 / 360

        if (self.navx.getYaw > 0):
            setpoint = self.navx.getYaw - (180 / 360)
        else:
            setpoint = self.navx.getYaw + (180 / 360)

        self.drivetrain.arcadeDrive(0, self.pid_angular.calculate(self.navx.getAngle(), setpoint))

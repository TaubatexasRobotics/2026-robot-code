import constants

from commands2 import Subsystem
from typing import Optional
from camera import AprilTagCamera
from phoenix5 import WPI_VictorSPX
from wpilib import MotorControllerGroup, DriverStation
from navx import AHRS
from wpilib.drive import DifferentialDrive
from wpimath.controller import PIDController
from wpimath.geometry import Pose2d
from pathplannerlib.auto import AutoBuilder
from pathplannerlib.controller import PPLTVController
from pathplannerlib.config import RobotConfig
from wpimath.kinematics import DifferentialDriveOdometry

class Drivetrain(Subsystem):
    def __init__(self) -> None:
        self.left_front_motor = WPI_VictorSPX(constants.kLeftFrontId)
        self.left_back_motor = WPI_VictorSPX(constants.kLeftBackId)
        self.right_front_motor = WPI_VictorSPX(constants.kRightFrontId)
        self.right_back_motor = WPI_VictorSPX(constants.kRightBackId)

        self.left_motors = MotorControllerGroup(self.left_front_motor,self.left_back_motor)
        self.right_motors = MotorControllerGroup(self.right_front_motor,self.right_back_motor)
        self.right_motors.setInverted(True)
        self.drivetrain = DifferentialDrive(self.left_motors,self.right_motors)

        self.navx = AHRS.create_spi()
        self.pid_angular = PIDController(0.1, 0, 0)
        self.pid_forward = PIDController(0.1, 0, 0)
        self.camera = AprilTagCamera(constants.kCameraName)

        self.pose = Pose2d()
        self.odometry = DifferentialDriveOdometry(
            self.gyro.getRotation2d(),

        )

        AutoBuilder.configure(
            self.getPose,
            self.resetPose,
            self.getRobotRelativeSpeeds,
            lambda: speeds, feedforwards: self.driveRobotRelative(speeds)
            PPLTVController(0.02),
            config,
            self.shouldFlipPath,
            self
        )

    def shouldFlipPath():
        return DriverStation.getAlliance() == DriverStation.Alliance.kRed

    def getPose(self) -> Pose2d:
        return self.pose
    
    def resetPose(self) -> None:
        

    def Front(self) -> None:
        self.drivetrain.tankDrive(1,1)

    def Back(self) -> None:
        self.drivetrain.tankDrive(-1,-1)

    def arcadeDrive(self, speed, rotate) -> None:
        self.drivetrain.arcadeDrive(speed, rotate)

    def tankDrive(self, left_speed, right_speed,) -> None:
        self.drivetrain.tankDrive(left_speed, right_speed)

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
        setpoint = 90 / 360

        self.drivetrain.arcadeDrive(0, self.pid_angular.calculate(self.navx.getAngle(), +setpoint))

    def turnTo90DegreesNegative(self, setpoint: Optional[int]) -> None:
        setpoint = 90 / 360

        self.drivetrain.arcadeDrive(0, self.pid_angular.calculate(self.navx.getAngle(), -setpoint))

    def turnTo180Degrees(self, setpoint: Optional[int]) -> None:
        setpoint = 180 / 360

        self.drivetrain.arcadeDrive(0, self.pid_angular.calculate(self.navx.getAngle(), setpoint))

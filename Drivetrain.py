import wpilib
import wpimath.controller
import rev
import wpilib.drive
import navx
import constants
from typing import Optional
import phoenix5
from camera import AprilTagCamera

class Drivetrain:
    def __init__(self) -> None:
        self.left_front_motor = phoenix5.WPI_VictorSPX(constants.kLeftFrontId)
        self.left_back_motor = phoenix5.WPI_VictorSPX(constants.kLeftBackId)
        self.right_front_motor = phoenix5.WPI_VictorSPX(constants.kRightFrontId)
        self.right_back_motor = phoenix5.WPI_VictorSPX(constants.kRightBackId)

        self.left_motors = wpilib.MotorControllerGroup(self.left_front_motor,self.left_back_motor)
        self.right_motors = wpilib.MotorControllerGroup(self.right_front_motor,self.right_back_motor)
        self.right_motors.setInverted(True)
        self.drivetrain = wpilib.drive.DifferentialDrive(self.left_motors,self.right_motors)

        self.navx = navx.AHRS.create_spi()
        self.pid_angular = wpimath.controller.PIDController(0.1, 0, 0)
        self.camera = AprilTagCamera("Camera7459")

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
import wpilib
import rev
import wpilib.drive
from wpilib import XboxController, SmartDashboard
from navx import AHRS
import wpimath

INITIAL_POSE = (0, 0, 0) # (x, y, theta)

C_RIGHT_FRONT = 50
C_RIGHT_BACK = 52
C_LEFT_FRONT = 55
C_LEFT_BACK = 54

SLOW_MODE_SPEED = 0.5
CONVERSION_FACTOR_METERS = 1/22.66

class Drivetrain():
    def __init__(self):
        self.left_front_motor = rev.SparkMax(C_LEFT_FRONT, rev.SparkLowLevel.MotorType.kBrushless)
        self.left_back_motor = rev.SparkMax(C_LEFT_BACK, rev.SparkLowLevel.MotorType.kBrushless)
        self.right_front_motor = rev.SparkMax(C_RIGHT_FRONT, rev.SparkLowLevel.MotorType.kBrushless)
        self.right_back_motor = rev.SparkMax(C_RIGHT_BACK, rev.SparkLowLevel.MotorType.kBrushless)

        self.left_motors = wpilib.MotorControllerGroup(self.left_front_motor,self.left_back_motor)
        self.right_motors = wpilib.MotorControllerGroup(self.right_front_motor,self.right_back_motor)
        self.Drivetrain = wpilib.drive.DifferentialDrive(self.left_motors,self.right_motors)
        self.left_motors.setInverted(True)
        self.joystick = XboxController(0)
        self.slow_mode = False
        self.speed_factor = 1
        
        self.setup_odometry()

    def setup_odometry(self):
        self.encoder_left = self.left_back_motor.getEncoder()
        self.encoder_right = self.right_back_motor.getEncoder()

        # self.encoder_left.setPositionConversionFactor(CONVERSION_FACTOR_METERS)
        # self.encoder_right.setPositionConversionFactor(CONVERSION_FACTOR_METERS)
        
        self.encoder_left.setPosition(0)
        self.encoder_right.setPosition(0)
        
        self.navx = AHRS.create_spi()
        self.navx.reset()
        
        self.field = wpilib.Field2d()
        
        rotation = wpimath.geometry.Rotation2d.fromDegrees(self.navx.getAngle())
        initial_pose = wpimath.geometry.Pose2d(*INITIAL_POSE)
        self.odometry = wpimath.kinematics.DifferentialDriveOdometry(rotation, 0, 0, initial_pose)
        
    def get_distance_meters(self) -> tuple[float, float]:        
        return (
            self.encoder_left.getPosition() * CONVERSION_FACTOR_METERS,
            self.encoder_right.getPosition()* CONVERSION_FACTOR_METERS
        )
        
    def get_velocity_mps(self) -> tuple[float, float]:
        return (
            self.encoder_left.getVelocity() * CONVERSION_FACTOR_METERS / 60,
            self.encoder_right.getVelocity()* CONVERSION_FACTOR_METERS / 60
        )

    def arcadeDrive(self,speed,rotate):
        self.Drivetrain.arcadeDrive(speed,rotate)
        
    def toggle_slow_mode(self):
        self.slow_mode = not self.slow_mode
        if self.slow_mode:
            self.speed_factor = 1
        else:
            self.speed_factor = SLOW_MODE_SPEED
            
    def update_odometry(self):
        rotation = wpimath.geometry.Rotation2d.fromDegrees(self.navx.getAngle())
        self.odometry.update(rotation, *self.get_distance_meters())
            
    def update_dashboard(self):
        self.update_odometry()
        # self.field.setRobotPose(self.get_pose())
        SmartDashboard.putData("Field", self.field)
        SmartDashboard.putBoolean("Slow mode", self.slow_mode)
        
    def triggers_to_axis(self):
        left = self.joystick.getLeftTriggerAxis()
        right = self.joystick.getRightTriggerAxis()
        
        return right - left
        
    def teleopPeriodic(self):
        if self.joystick.getXButtonPressed():
            self.toggle_slow_mode()
        
        self.Drivetrain.arcadeDrive(
            self.triggers_to_axis() * self.speed_factor,
            self.joystick.getRawAxis(1) * self.speed_factor
        )


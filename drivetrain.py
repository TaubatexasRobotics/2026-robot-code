import wpilib
import rev
import wpilib.drive
from wpilib import XboxController


C_RIGHT_FRONT = 50
C_RIGHT_BACK = 52
C_LEFT_FRONT = 55
C_LEFT_BACK = 54

SLOW_MODE_SPEED = 0.5

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
        self.joystick = wpilib.XboxController(0)
        self.slow_mode = False
        self.speed_factor = 1

    def arcadeDrive(self,speed,rotate):
        self.Drivetrain.arcadeDrive(speed,rotate)
        
    def toggle_slow_mode(self):
        self.slow_mode = not self.slow_mode
        if self.slow_mode:
            self.speed_factor = 1
        else:
            self.speed_factor = SLOW_MODE_SPEED
        
    def teleopPeriodic(self):
        
        
        self.Drivetrain.arcadeDrive(
            self.joystick.getRawAxis(1) * self.speed_factor,
            self.joystick.getRawAxis(0) * self.speed_factor
        )


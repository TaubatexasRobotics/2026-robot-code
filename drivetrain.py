import wpilib
import rev
import wpilib.drive

C_RIGHT_FRONT = 7
C_RIGHT_BACK = 9
C_LEFT_FRONT = 10
C_LEFT_BACK = 8

class Drivetrain():
    def __init__(self):
        self.left_front_motor = rev.SparkMax(C_LEFT_FRONT, rev.SparkLowLevel.MotorType.kbrushless)
        self.left_back_motor = rev.SparkMax(C_LEFT_BACK, rev.SparkLowLevel.MotorType.kbrushless)
        self.right_front_motor = rev.SparkMax(C_RIGHT_FRONT, rev.SparkLowLevel.MotorType.kbrushless)
        self.right_back_motor = rev.SparkMax(C_RIGHT_BACK, rev.SparkLowLevel.MotorType.kbrushless)

        self.left_motors = wpilib.MotorControllerGroup(self.left_front_motor,self.left_back_motor)
        self.right_motors = wpilib.MotorControllerGroup(self.right_front_motor,self.right_back_motor)
        self.Drivetrain = wpilib.drive.DifferentialDrive(self.left_motors,self.right_motors)
        self.left_motors.setInverted(True)

    def arcadeDrive(self,speed,rotate):
        self.Drivetrain.arcadeDrive(speed,rotate)


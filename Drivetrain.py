import wpilib
import rev
import wpilib.drive

class Drivetrain():
    def __init__(self):
        self.left_front_motor = rev.SparkMax(1, rev.SparkLowLevel.MotorType.kbrushless)
        self.left_back_motor = rev.SparkMax(1, rev.SparkLowLevel.MotorType.kbrushless)
        self.right_front_motor = rev.SparkMax(1, rev.SparkLowLevel.MotorType.kbrushless)
        self.right_back_motor = rev.SparkMax(1, rev.SparkLowLevel.MotorType.kbrushless)

        self.left_motors = wpilib.MotorControllerGroup(self.left_front_motor,self.left_back_motor)
        self.right_motors = wpilib.MotorControllerGroup(self.right_front_motor,self.right_back_motor)
        self.Drivetrain = wpilib.drive.DifferentialDrive(self.left_motors,self.right_motors)
        self.left_motors.setInverted(True)

    def arcadeDrive(self,speed,rotate):
        self.Drivetrain.arcadeDrive(speed,rotate)


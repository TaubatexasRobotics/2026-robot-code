import wpilib
from commands2 import TimedCommandRobot
from RampJoystick import RampJoystick
from phoenix5 import WPI_VictorSPX
from wpilib.drive import DifferentialDrive

class MyRobot(TimedCommandRobot):

    def robotInit(self):
        self.joystick = RampJoystick(0,0.5,0.7,0.8,0.2)
        self.motor1 = WPI_VictorSPX(1)
        self.motor2 = WPI_VictorSPX(2)
        self.motor3 = WPI_VictorSPX(3)
        self.motor4 = WPI_VictorSPX(4)

        self.rightMotors = wpilib.MotorControllerGroup(self.motor1, self.motor2)
        self.leftMotors = wpilib.MotorControllerGroup(self.motor3, self.motor4)

        self.drivetrain = DifferentialDrive(self.leftMotors, self.rightMotors)
        

    def teleopInit(self):
        return super().teleopInit()

    def teleopPeriodic(self):
        self.drivetrain.arcadeDrive(self.joystick.getRampAxis(1), self.joystick.getRampAxis(0),False)
        #self.motor1.set(self.joystick.getRampAxis(1))
        #self.motor2.set(self.joystick.getRampAxis(0))
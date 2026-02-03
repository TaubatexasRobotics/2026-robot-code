from rev import SparkMax, SparkLowLevel
from phoenix5 import WPI_VictorSPX
import constants

class Intake:
    def __init__(self):
        self.arm_motor = SparkMax(constants.kIntakeAngleMotor, SparkLowLevel.MotorType.kBrushless)
        self.roll_motor = WPI_VictorSPX(constants.kIntakeTrackMotor)

        self.encoder = self.arm_motor.getEncoder()

    def turnDown(self):
        self.arm_motor.set(-0.7)

    def stopArm(self):
        self.arm_motor.set(0)   

    def turnUp(self):
        self.arm_motor.set(0.7)    

    def suckBalls(self):    
        self.roll_motor.set(-1)

    def stopRoll(self):
        self.roll_motor.set(0)    

    def dropBalls(self):
        self.roll_motor.set(1)
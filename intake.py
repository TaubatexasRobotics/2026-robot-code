import rev
import phoenix5

class Intake:
    def __init__(self):
        self.arm_motor = rev.SparkMax(53, rev.SparkLowLevel.MotorType.kBrushless)
        self.roll_motor = phoenix5.WPI_VictorSPX(12)

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
import rev
import phoenix5

ARM_MOTOR_ID = 53
ROLL_MOTOR_ID = 12

class Intake:
    def __init__(self):
        self.arm_motor = rev.SparkMax(ARM_MOTOR_ID, rev.SparkLowLevel.MotorType.kBrushless)
        self.roll_motor = phoenix5.WPI_VictorSPX(ROLL_MOTOR_ID)

    def turnDown(self):
        self.arm_motor.set(-0.7)

    def stopArm(self):
        self.arm_motor.set(0)   

    def turnUp(self):
        self.arm_motor.set(0.7)    

    def receive(self):    
        self.roll_motor.set(-1)

    def stopRoll(self):
        self.roll_motor.set(0)    

    def drop(self):
        self.roll_motor.set(1)
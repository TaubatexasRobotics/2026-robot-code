import rev
import phoenix5
import wpilib
from wpilib import SmartDashboard

ARM_MOTOR_ID = 53
ROLL_MOTOR_ID = 12

joystick = wpilib.Joystick(0)

class Intake:
    def __init__(self):
        self.is_enabled = False
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
        
    def teleopPeriodic(self):
        try:
            if joystick.getRawButtonPressed(1):
                self.is_enabled = not self.is_enabled  

            if self.is_enabled:
                self.receive()
            else:
                if joystick.getRawButton(4):
                    self.drop()
                else:
                    self.stopRoll()

            if joystick.getRawButton(2):
                self.turnDown()
            elif joystick.getRawButton(3):
                self.turnUp()
            else:
                self.stopArm()
                
        except BaseException as e:
            wpilib.DataLogManager.log(repr(e))
import phoenix5
from wpilib import SmartDashboard, XboxController

PIVOT_MOTOR_ID = 4
ROLL_MOTOR_ID = 1

joystick = XboxController(0)

class Intake:
    def __init__(self):
        self.is_enabled = False
        self.pivot_motor = phoenix5.WPI_VictorSPX(PIVOT_MOTOR_ID)
        self.roll_motor = phoenix5.WPI_VictorSPX(ROLL_MOTOR_ID)
        
    def update_dashboard(self):
        SmartDashboard.putBoolean("Intake/intake enabled", self.is_enabled)
        
    def turnDown(self):
        self.pivot_motor.set(-0.7)

    def stopArm(self):
        self.pivot_motor.set(0)   

    def turnUp(self):
        self.pivot_motor.set(0.7)    

    def receive(self):    
        self.roll_motor.set(-1)

    def stopRoll(self):
        self.roll_motor.set(0)    

    def drop(self):
        self.roll_motor.set(1)
        
    def teleopPeriodic(self):
        if joystick.getBButtonPressed():
            self.is_enabled = not self.is_enabled  

        if self.is_enabled:
            self.receive()
        
        else:
            if joystick.getXButton():
                self.drop()
            else:
                self.stopRoll()

        if joystick.getAButton():
            self.turnDown()
        elif joystick.getYButton():
            self.turnUp()
        else:
            self.stopArm()
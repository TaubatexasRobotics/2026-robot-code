import phoenix5
from wpilib import SmartDashboard, XboxController

PIVOT_MOTOR_ID = 4
ROLL_MOTOR_ID = 1


class Intake:
    def __init__(self):
        self.is_enabled = False
        self.pivot_motor = phoenix5.WPI_VictorSPX(PIVOT_MOTOR_ID)
        self.roll_motor = phoenix5.WPI_VictorSPX(ROLL_MOTOR_ID)
        
        self.joystick = XboxController(0)
        
    def update_dashboard(self):
        SmartDashboard.putBoolean("Intake/intake enabled", self.is_enabled)
        SmartDashboard.putNumber("Intake/pivot motor", self.pivot_motor.get())
        SmartDashboard.putNumber("Intake/roll motor", self.roll_motor.get())
        
    def pivotDown(self):
        self.pivot_motor.set(-0.7)

    def stopArm(self):
        self.pivot_motor.set(0)   

    def pivotUp(self):
        self.pivot_motor.set(0.7)    

    def receive(self):    
        self.roll_motor.set(-1)

    def stopRoll(self):
        self.roll_motor.set(0)    

    def drop(self):
        self.roll_motor.set(1)
        
    def teleopPeriodic(self):
        if self.joystick.getXButtonPressed():
            self.is_enabled = not self.is_enabled  

        if self.is_enabled:
            self.receive()
            
        if not self.is_enabled:
            self.stopRoll()
            
        if self.joystick.getYButton():
            self.is_enabled = False
            self.drop()

        pov = self.joystick.getPOV()

        #TODO -> use or logic to also accept diagonals (eg. POVDownLeft and POVDownRight)
        if pov in (180, 135, 225):
            self.pivotDown()
        elif pov in (0, 45, 315):
            self.pivotUp()
        else:
            self.stopArm()
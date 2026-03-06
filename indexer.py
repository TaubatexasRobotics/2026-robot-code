import phoenix5
from wpilib import SmartDashboard, XboxController

REDLINE_MOTOR_ID = 5

class Indexer():
    def __init__(self):
        self.joystick = XboxController(1)
        self.antijam_motor = phoenix5.WPI_VictorSPX(REDLINE_MOTOR_ID)
    
    def update_dashboard(self):
        SmartDashboard.putBoolean("Indexer/redline enabled", self.antijam_motor.get())
        SmartDashboard.putNumber("Indexer/redline", self.antijam_motor.get())
        
    def send_balls(self):
        self.antijam_motor.set(-.15)
        
    def release_balls(self):
        self.antijam_motor.set(.15)
        
    def stop(self):
        self.antijam_motor.set(0)
    
    def teleopPeriodic(self):
        if self.joystick.getXButton():
            self.send_balls()
        elif self.joystick.getYButton():
            self.release_balls()
        else:
            self.stop()
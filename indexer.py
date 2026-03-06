import phoenix5
from wpilib import SmartDashboard, XboxController

CIM_MOTOR_ID = 2
REDLINE_MOTOR_ID = 5

class Indexer():
    def __init__(self):
        self.cim = phoenix5.WPI_VictorSPX(CIM_MOTOR_ID)
        self.redline = phoenix5.WPI_VictorSPX(REDLINE_MOTOR_ID)
        
        SmartDashboard.putNumber("Indexer/cim", 0)
        SmartDashboard.putBoolean("Indexer/cim enabled", True)
        SmartDashboard.putNumber("Indexer/redline", 0)
        SmartDashboard.putBoolean("Indexer/redline enabled", True)

        self.joystick = XboxController(1)
    
    def update_dashboard(self):
        SmartDashboard.putBoolean("Indexer/cim enabled", self.cim.get())
        SmartDashboard.putBoolean("Indexer/redline enabled", self.redline.get())
        SmartDashboard.putNumber("Indexer/cim", self.cim.get())
        SmartDashboard.putNumber("Indexer/redline", self.redline.get())
    
    def is_motor_enabled(self):
        return self.cim.get() != 0 or self.redline.get() != 0
    
    def send_balls(self):
        self.cim.set(-1)
        self.redline.set(-.15)
        
    def release_balls(self):
        self.cim.set(1)
        self.redline.set(.15)
        
    def stop(self):
        self.cim.set(0)
        self.redline.set(0)
    
    def teleopPeriodic(self):
        if self.joystick.getXButton():
            self.send_balls()
        elif self.joystick.getYButton():
            self.release_balls()
        else:
            self.stop()
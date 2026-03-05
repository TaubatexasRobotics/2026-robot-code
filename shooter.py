import rev
from wpilib import XboxController, SmartDashboard

SHOOTER_MOTOR_ID = 51

class Shooter():  
    def __init__(self):
        self.motor = rev.SparkMax(SHOOTER_MOTOR_ID, rev.SparkLowLevel.MotorType.kBrushless)
        self.is_enabled = False
        self.joystick = XboxController(1)
        
    def update_dashboard(self):
        SmartDashboard.putBoolean("Shooter/shooter enabled", self.is_enabled)
    
    def shoot(self, speed) -> None:
        self.motor.set(speed)
        
    def teleopPeriodic(self):
        if self.joystick.getRightBumperButtonPressed():
            self.is_enabled = not self.is_enabled
        
        if self.is_enabled:
            self.shoot(-1)
        else:
            self.shoot(0)
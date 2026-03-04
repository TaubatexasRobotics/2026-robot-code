from wpilib import SmartDashboard
import rev
from wpimath.controller import PIDController

YAW_MOTOR_ID = 56

class Turret:
    def __init__(self):
        self.yaw = rev.SparkMax(YAW_MOTOR_ID, rev.SparkLowLevel.MotorType.kBrushless)
        self.yaw_encoder = self.yaw.getEncoder()
        self.pid = PIDController(.01, .0, .0)
        SmartDashboard.putData("Turret/PID", self.pid)        
        
    def update_dashboard(self):
        SmartDashboard.putNumber("Turret/yaw encoder", self.yaw.getEncoder().getPosition())
        SmartDashboard.putData("Turret/PID", self.pid)

    def yaw(self, speed) -> None:
        self.yaw.set(speed)


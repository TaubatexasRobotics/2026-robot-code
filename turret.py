from wpilib import SmartDashboard, XboxController
import rev
from wpimath.controller import PIDController

YAW_MOTOR_ID = 56

class Turret:
    def __init__(self):
        self.yaw_motor = rev.SparkMax(YAW_MOTOR_ID, rev.SparkLowLevel.MotorType.kBrushless)
        self.yaw_encoder = self.yaw_motor.getEncoder()
        self.pid = PIDController(.01, .0, .0)
        SmartDashboard.putData("Turret/PID", self.pid)
        self.joystick = XboxController(0)      
        
    def update_dashboard(self):
        SmartDashboard.putNumber("Turret/yaw encoder", self.yaw_motor.getEncoder().getPosition())
        SmartDashboard.putData("Turret/PID", self.pid)
        SmartDashboard.putNumber("Turret/yaw", self.yaw_motor.get())
        SmartDashboard.putNumber("Turret/left x axis", self.joystick.getLeftX())
        SmartDashboard.putNumber("Turret/Motor", self.yaw_motor.get())
        
    def teleopPeriodic(self):
        self.yaw_motor.set(self.joystick.getLeftX())

    def yaw_motor(self, speed) -> None:
        self.yaw_motor.set(speed)


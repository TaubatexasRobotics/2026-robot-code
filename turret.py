from wpilib import SmartDashboard, Joystick
from utils import clamp
import rev
from wpimath.controller import PIDController
from camera import PhotonVisionCamera

YAW_MOTOR_ID = 56

class Turret:
    def __init__(self):
        self.motor = rev.SparkMax(YAW_MOTOR_ID, rev.SparkLowLevel.MotorType.kBrushless)
        self.motor_encoder = self.motor.getEncoder()
        self.pid = PIDController(0.001, 0, 0)
        SmartDashboard.putData("Turret/PID", self.pid)  
        self.camera = PhotonVisionCamera("camera ps3")      
        self.joystick = Joystick(0)
        
    def update_dashboard(self):
        SmartDashboard.putNumber("Turret/yaw encoder", self.motor.getEncoder().getPosition())
        SmartDashboard.putData("Turret/PID", self.pid)

    def yaw(self, speed) -> None:
        self.motor.set(speed)

    def followTagYaw(self):
        target = self.camera.getBestTarget()
        yaw = target.getYaw()
        print(yaw)
        result = clamp(self.pid.calculate(yaw, 0), -1,1)
        self.motor.setVoltage(result * 12)
    
    def teleopPeriodic(self):
        if self.joystick.getRawButton(5):
            self.followTagYaw()
        else:
            self.motor.setVoltage(0)

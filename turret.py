import wpilib
from wpilib import SmartDashboard
import rev
import phoenix6
from wpimath.controller import PIDController
import wpimath.controller


SHOOTER_MOTOR_ID = 7
PITCH_MOTOR_ID = 11
YAW_MOTOR_ID = 9

# PITCH_ID = 10

PITCH_ENCODER_INITIAL_POSITION = 0.3394665395

class Turret:
    def __init__(self):
        self.yaw = rev.SparkMax(YAW_MOTOR_ID, rev.SparkLowLevel.MotorType.kBrushless)
        self.pitch = rev.SparkMax(PITCH_MOTOR_ID, rev.SparkLowLevel.MotorType.kBrushless)
        
        self.pitch_encoder = self.pitch.getEncoder()
        self.pitch_pid = PIDController(0.1, 0, 0)
        self.pitch_pid.setTolerance(0.1)
        self.pitch_encoder.setPosition(PITCH_ENCODER_INITIAL_POSITION)
        
        self.shooter = phoenix6.hardware.TalonFX(SHOOTER_MOTOR_ID, "rio")
        
    def update_dashboard(self):
        SmartDashboard.putData(self.pitch_pid)
        SmartDashboard.putNumber("crest encoder (rad)", self.pitch_encoder.getPosition())
        SmartDashboard.putNumber("crest encoder (degrees)", float(self.pitch_encoder.getPosition()))
    # self.pid.setSetpoint(self.setpoint)    

    def shooterSpeed(self, speed) -> None:
        self.shooter.set(speed)

    def yaw(self, speed) -> None:
        self.yaw.set(speed)
        
    def pitch(self, voltage) -> None:
        self.pitch.setVoltage(5)

    # def pitchUp(self) -> None:
    #     self.pitch.set(1)

    # def pitchDown(self) -> None:
    #     self.pitch.set(-1)    
    
    # def aimAtTarget(self, tag : int) -> None:
    #     yaw = self.camera.getYaw(tag)
    #     turn = self.pid_angular.calculate(yaw, 0) if yaw != -1 else 0
    #     self.yaw.set(turn)
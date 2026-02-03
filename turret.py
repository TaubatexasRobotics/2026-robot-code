import wpilib
import rev
import phoenix6
from wpimath.controller import PIDController

SHOOTER_MOTOR_ID = 7
YAW_MOTOR_ID = 9
# PITCH_ID = 10

class Turret:
    def __init__(self):
        self.yaw = rev.SparkMax(YAW_MOTOR_ID, rev.SparkLowLevel.MotorType.kBrushless)
        self.shooter = phoenix6.hardware.TalonFX(SHOOTER_MOTOR_ID, "rio")
        # self.pitch = rev.SparkMax(PITCH_ID, rev.SparkLowLevel.MotorType.kBrushless)

    def shooterSpeed(self, speed) -> None:
        self.shooter.set(speed)

    def yaw(self, speed) -> None:
        self.yaw.set(speed)

    # def pitchUp(self) -> None:
    #     self.pitch.set(1)

    # def pitchDown(self) -> None:
    #     self.pitch.set(-1)    
    
    # def aimAtTarget(self, tag : int) -> None:
    #     yaw = self.camera.getYaw(tag)
    #     turn = self.pid_angular.calculate(yaw, 0) if yaw != -1 else 0
    #     self.yaw.set(turn)
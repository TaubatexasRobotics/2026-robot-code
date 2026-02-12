from phoenix6.hardware import TalonFX
from camera import Camera
from wpimath.controller import PIDController
import rev


class Turret:
    def __init__(self):
        self.yaw = rev.SparkMax(51, rev.SparkMax.MotorType.kBrushless)
        self.pid_angular = PIDController(0.05, 0, 0)

    def yawLeft(self):
        self.yaw.set(1)

    def yawRight(self):
        self.yaw.set(-1)

    def stop(self):
        self.yaw.set(0)

    def turretAlign(self, tag: int, camera: Camera) -> None:
        tag_yaw = camera.getYawFromTag(tag)
        turn = self.pid_angular.calculate(tag_yaw, 0) if tag_yaw != -1 else 0
        self.yaw.set(turn)

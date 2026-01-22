import wpilib
import rev
import phoenix6
from camera import AprilTagCamera
from wpimath.controller import PIDController

class Turret:
    def __init__(self, motor_port):
        self.shooter1 = rev.SparkMax(1, rev.SparkLowLevel.MotorType.kBrushless)
        self.shooter2 = rev.SparkMax(1, rev.SparkLowLevel.MotorType.kBrushless)
        self.yaw = phoenix6.hardware.TalonFX(1, "rio")
        self.pitch = rev.SparkMax(1, rev.SparkLowLevel.MotorType.kBrushless)

        self.shooter = wpilib.MotorControllerGroup(self.shooter1, self.shooter2)
        self.shooter1.setInverted(True)

        self.camera = AprilTagCamera()
        self.pid_angular = PIDController(0.1, 0, 0)


    def shooterSpeed(self, speed) -> None:
        self.shooter.set(speed)

    def yawLeft(self) -> None:
        self.yaw.set(1)

    def yawRight(self):    
        self.yaw.set(-1)

    def pitchUp(self) -> None:
        self.pitch.set(1)

    def pitchDown(self) -> None:
        self.pitch.set(-1)    
    
    def aimAttTarget(self, tag : int) -> None:
        yaw = self.camera.getYaw(tag)
        turn = self.pid_angular.calculate(yaw, 0) if yaw != -1 else 0
        self.yaw.set(turn)
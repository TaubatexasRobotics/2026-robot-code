import wpilib
import rev
import phoenix6
import wpimath.controller
from camera import AprilTagCamera


class Turret:
    def __init__(self, camera):
        self.shooter1 = rev.SparkMax(1, rev.SparkLowLevel.MotorType.kBrushless)
        self.shooter2 = rev.SparkMax(2, rev.SparkLowLevel.MotorType.kBrushless)
        self.kraken = phoenix6.hardware.TalonFX(20)
        self.pitch = rev.SparkMax(3, rev.SparkLowLevel.MotorType.kBrushless)

        self.shooter = wpilib.MotorControllerGroup(self.shooter1, self.shooter2)
        self.shooter1.setInverted(True)
        self.pid_angular = wpimath.controller.PIDController(0.1, 0, 0)
        self.pid_forward = wpimath.controller.PIDController(0.1, 0, 0)
        self.camera = AprilTagCamera("Camera7459")

    def shooterSpeed(self, speed):
        self.shooter.set(speed)

    def yawLeft(self):
        self.kraken.set(1)

    def yawRight(self):    
        self.kraken.set(-1)
    
    def turnOffKraken(self):
        self.kraken.set(0)

    def pitchUp(self):
        self.pitch.set(1)

    def pitchDown(self):
        self.pitch.set(-1)    
        
    def TurretAlign(self, tag: int) -> None:
        yaw = self.camera.getYaw(tag)
        turn = self.pid_angular.calculate(yaw, 0) if yaw != -1 else 0
        self.kraken.set(turn)
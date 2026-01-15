import wpilib
import rev
import phoenix6


class Turret:
    def __init__(self, motor_port):
        self.shooter1 = rev.SparkMax(1, rev.SparkLowLevel.MotorType.kBrushless)
        self.shooter2 = rev.SparkMax(1, rev.SparkLowLevel.MotorType.kBrushless)
        self.yaw = phoenix6.hardware.TalonFX(1, "Kraken")
        self.pitch = rev.SparkMax(1, rev.SparkLowLevel.MotorType.kBrushless)

        self.shooter = wpilib.MotorControllerGroup(self.shooter1, self.shooter2)
        self.shooter1.setInverted(True)

    def shooterSpeed(self, speed):
        self.shooter.set(speed)

    def yawLeft(self):
        self.yaw.set(1)

    def yawRight(self):    
        self.yaw.set(-1)

    def pitchUp(self):
        self.pitch.set(1)

    def pitchDown(self):
        self.pitch.set(-1)    
        
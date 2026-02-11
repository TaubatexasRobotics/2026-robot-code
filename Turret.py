import rev
import wpimath.controller

class Turret:
    def __init__(self):
        self.turret_motor = rev.SparkMax(
            51, rev.SparkLowLevel.MotorType.kBrushless
        )
        self.encoder = self.turret_motor.getEncoder()
        self.pid = wpimath.controller.PIDController(0.00025, 0, 0)
        self.target_RPM = 4500
        self.pid.setTolerance(100)

    def shoot(self):
        self.target_RPM = 4500

    def stop(self):
        self.target_RPM = 0
        self.turret_motor.stopMotor()
        self.pid.reset()

    def update(self):
        if self.target_RPM == 0:
            return

        output = self.pid.calculate(
            self.encoder.getVelocity(),
            self.target_RPM
        )

        output = max(min(output, 1.0), -1.0)
        self.turret_motor.set(output)

    def isReady(self):
        return abs(self.encoder.getVelocity() - self.target_RPM) < 100
    

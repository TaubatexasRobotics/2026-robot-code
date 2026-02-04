import rev

class Turret:
    def __init__(self):
        self.turret_motor = rev.SparkMax(51, rev.SparkLowLevel.MotorType.kBrushless)
      
    def turnLeft(self):
        self.turret_motor.set(0.2)

    def turnRight(self):
        self.turret_motor.set(-0.2)

    def stopTurret(self):
        self.turret_motor.set(0)       
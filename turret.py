from rev import SparkMax, SparkLowLevel
from wpimath.controller import PIDController, SimpleMotorFeedforwardRadians
from commands2 import Subsystem, command


class Turret(Subsystem):
    def __init__(self):
        self.turret_motor = SparkMax(51, SparkLowLevel.MotorType.kBrushless)
        self.encoder = self.turret_motor.getEncoder()
        self.pid = PIDController(0.00025, 0, 0)
        self.pid.setTolerance(0.1)
        # self.target_RPM = 4500
        self.feedforward = SimpleMotorFeedforwardRadians(0, 0.002)
    
    def normalize(pixels, max_pixels):
        return (pixels * 2 / max_pixels) -1

    def clamp(self,value, min_value, max_value):
        return max(min(value, max_value), min_value)

    def centerTurret(self, alignment):
            #normalized_alignment = self.normalize(alignment, 1080)#chutando que a camera tem 1080

            output = self.pid.calculate(alignment, 0)

            output = self.clamp(output, -1,1)

            self.turret_motor.setVoltage(output * 12)

    def commandCenterTurret(self,alignment) -> command:
         return self.run(lambda: self.centerTurret(alignment))
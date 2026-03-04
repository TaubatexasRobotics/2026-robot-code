from rev import SparkMax, SparkLowLevel
from wpimath.controller import PIDController, SimpleMotorFeedforwardRadians
from commands2 import Subsystem, command
from camera import PhotonVisionCamera

class Turret(Subsystem):
    def __init__(self):
        super().__init__()
        self.turret_motor = SparkMax(56, SparkLowLevel.MotorType.kBrushless)
        self.encoder = self.turret_motor.getEncoder()
        self.pid = PIDController(0.0001, 0, 0)
        self.pid.setTolerance(0.1)
        self.setDefaultCommand(self.deactivate())
        # self.target_RPM = 4500

    def clamp(self,value, min_value, max_value):
        return max(min(value, max_value), min_value)
    
    def deactivate(self) -> command:
        return self.run(lambda: self.turret_motor.set(0))
    
    def centerTurret(self, alignment):
            #normalized_alignment = alignment / 180

            output = self.pid.calculate(alignment, 0)

            output = self.clamp(output, -1,1)

            self.turret_motor.setVoltage(alignment*12)

    def commandCenterTurret(self,camera: PhotonVisionCamera) -> command:
        return self.run(lambda: self.centerTurret(camera.getBestTarget().getYaw()))
    
    
    def periodic(self):
        print(self.getCurrentCommand())
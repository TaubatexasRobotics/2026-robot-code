from rev import SparkMax, SparkLowLevel
from wpimath.controller import PIDController, SimpleMotorFeedforwardRadians
from commands2 import Subsystem, Command, ParallelCommandGroup
from utils import Utils
from camera import AprilTagCamera
from typing import Callable, Optional
from led import LEDController
import constants


class Turret(Subsystem):
    def __init__(self):
        self.yaw = SparkMax(constants.kTurretId, SparkLowLevel.MotorType.kBrushless)
        self.encoder = self.yaw.getEncoder()
        self.pid = PIDController(0.05, 0, 0)
        self.pid.setTolerance(0.1)
        # self.target_RPM = 4500
        self.feedforward = SimpleMotorFeedforwardRadians(0, 0.002)
    
    def activateYawClockwise(self) -> Command:
        return self.run(lambda: self.yaw.set(0.5))

    def activateYaw(self, rotate: Callable[[], float]) -> Command:
        return self.run(lambda: self.yaw.set(rotate()))

    def followYawTag(self, camera: AprilTagCamera, led: Optional[LEDController]=None) -> Command:
        yaw = camera.getYawFromBestTarget()
        rotation = 0
        if yaw != -1:
            rotation = self.pid.calculate(yaw, 0) 
            if led is not None:
                return ParallelCommandGroup(
                        led.blinkGreen(),
                        self.run(lambda: self.yaw.set(rotation))
                    )

        if led is not None:
            return ParallelCommandGroup(
                    led.red(),
                    self.run(lambda: self.yaw.set(rotation))
                )

        return self.run(lambda: self.yaw.set(rotation))

    def stopYaw(self) -> Command:
        return self.run(lambda: self.yaw.set(0))

    def activateYawCounterClockwise(self) -> Command:
        return self.run(lambda: self.yaw.set(-0.5))

    def clamp(self,value, min_value, max_value):
        return max(min(value, max_value), min_value)

    def centerTurret(self, alignment):
        normalized_alignment = Utils.normalize(alignment, 1080) #chutando que a camera tem 1080

        output = self.pid.calculate(alignment, 0)

        output = self.clamp(output, -1,1)

        self.yaw.setVoltage(output * 12)

    def commandCenterTurret(self,alignment) -> Command:
        return self.run(lambda: self.centerTurret(alignment))
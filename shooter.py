from rev import (
    SparkMax,
    SparkLowLevel,
    ResetMode,
    PersistMode,
    SparkMaxConfig,
    SparkBaseConfig,
)
from commands2 import Subsystem, Command
from camera import AprilTagCamera
from wpimath.controller import PIDController
import constants

class Shooter(Subsystem):
    def __init__(self) -> None:
        self.flywheel = SparkMax(
            constants.kFlywheelId, SparkLowLevel.MotorType.kBrushless
        )
        self.hood = SparkMax(constants.kHoodId, SparkMax.MotorType.kBrushless)
        self.hood_encoder = self.hood.getEncoder()

        self.hood_pid = PIDController(0.006, 0.0, 0.0)
        self.hood_pid.setTolerance(0.1)
        self.hood_encoder.setPosition(0)

        config = SparkMaxConfig()

        config.smartCurrentLimit(30)
        config.setIdleMode(SparkBaseConfig.IdleMode.kCoast)

        self.flywheel.configure(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )
        self.hood.configure(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )

        self.setDefaultCommand(self.deactivateFlywheel())

    def activateFlywheel(self) -> Command:
        return self.run(lambda: self.flywheel.set(0.4))

    def deactivateFlywheel(self) -> Command:
        return self.run(lambda: self.flywheel.set(0))

    def hoodUp(self) -> Command:
        return self.run(lambda: self.hood.set(0.5))

    def hoodDown(self) -> Command:
        return self.run(lambda: self.hood.set(-0.5))
    
    def openHoodByDistanceOfTag(self, camera: AprilTagCamera) -> Command:
        range = camera.getRangeFromBestTarget()
        rotation = self.hood_pid.calculate(range, 0)
        return self.run(lambda: self.hood.set(rotation))
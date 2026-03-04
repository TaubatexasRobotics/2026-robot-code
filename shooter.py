from rev import (
    SparkMax,
    SparkLowLevel,
    ResetMode,
    PersistMode,
    SparkMaxConfig,
    SparkBaseConfig,
)
from commands2 import Subsystem, Command
from wpilib import SmartDashboard
from wpimath.controller import (
    BangBangController,
    SimpleMotorFeedforwardMeters,
    PIDController,
)
from wpimath.units import rotationsPerMinuteToRadiansPerSecond
import constants
from utils import Utils

gear_ratio = 11.52

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

        config.smartCurrentLimit(40)
        config.setIdleMode(SparkBaseConfig.IdleMode.kCoast)

        self.flywheel.configure(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )
        self.hood.configure(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )

        self.setDefaultCommand(self.deactivateFlywheel())

    def periodic(self) -> None:
        SmartDashboard.putData("PID", self.hood_pid)
        SmartDashboard.putNumber("crest encoder", self.hood_encoder.getPosition())
        SmartDashboard.putNumber("crest position", float(self.getPosition()))

    def getPosition(self) -> float:
        return self.hood_encoder.getPosition() * gear_ratio * 360

    def moveToSetpoint(self):
        current_position = self.getPosition()
        hood_value = self.hood_pid.calculate(current_position)
        hood_value = Utils.clamp(hood_value, -0.4, 0.4)
        self.hood.set(hood_value)

    def moveTo(self, setpoint):
        current_position = self.getPosition()
        hood_value = self.hood_pid.calculate(current_position, setpoint)
        hood_value = Utils.clamp(hood_value, -0.4, 0.4)
        self.hood.set(hood_value)

    def up(self):
        self.moveTo(20)

    def down(self):
        self.moveTo(0)

    def activateFlywheel(self) -> Command:
        return self.run(lambda: self.flywheel.set(0.2))

    def deactivateFlywheel(self) -> Command:
        return self.run(lambda: self.flywheel.set(0))
    
    def commandMoveToSetpoint(self) -> Command:
        return self.run(lambda: self.moveToSetpoint)
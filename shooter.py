from rev import (
    SparkMax,
    SparkLowLevel,
    ResetMode,
    PersistMode,
    SparkMaxConfig,
    SparkBaseConfig,
)
from commands2 import Subsystem
from wpilib import SmartDashboard
from wpimath.controller import BangBangController
import constants


class Shooter(Subsystem):
    flywheel: SparkMax = SparkMax(11, SparkLowLevel.MotorType.kBrushless)
    bangBangController: BangBangController = BangBangController()

    def __init__(self) -> None:
        config = SparkMaxConfig()

        config.smartCurrentLimit(40)
        config.setIdleMode(SparkBaseConfig.IdleMode.kCoast)
        config.closedLoop.feedForward.sva(*constants.kFlywheelFeedForward)

        self.flywheel.configure(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )

        self.closedLoopController = self.flywheel.getClosedLoopController()
        SmartDashbotad.putData(self.bangBangController)

    def activateFlywheel(self) -> None:
        self.motor.set(0.7)
    
    def 
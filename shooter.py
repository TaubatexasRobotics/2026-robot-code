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
from wpimath.controller import PIDController, ArmFeedforward
import constants
from wpilib import SmartDashboard, SendableChooser

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
        config.setIdleMode(SparkBaseConfig.IdleMode.kBrake)

        self.flywheel.configure(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )
        self.hood.configure(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )

        self.setDefaultCommand(self.run(lambda: self.deactivate()))
        self.armFeedForward = ArmFeedforward(1.2,1,1)

    def activateFlywheel(self) -> Command:
        return self.run(lambda: self.flywheel.set(0.4))
    
    def activateFlywheel100(self) -> Command:
        return self.run(lambda: self.flywheel.set(0.7))
    
    def activateFlywheel75(self) -> Command:
        return self.run(lambda: self.flywheel.set(0.6))
    
    def activateFlywheel50(self) -> Command:
        return self.run(lambda: self.flywheel.set(0.5))
    
    
    def deactivateFlywheel(self) -> Command:
        return self.run(lambda: self.flywheel.set(0))

    def deactivate(self) -> None:
        self.flywheel.set(0)
        self.hood.set(0)
    
    def hoodDown(self) -> Command:
        return self.run(lambda: self.hood.set(0.1))

    def hoodUp(self) -> Command:
        return self.run(lambda: self.hood.set(-0.5))
    
    def hoopUp_025(self) -> Command:
        return self.run(lambda: self.hood.getClosedLoopController().setSetpoint(0.25))
    
    def openHoodByDistanceOfTag(self, camera: AprilTagCamera) -> Command:
        range = camera.getRangeFromBestTarget()
        rotation = self.hood_pid.calculate(range, 0)
        return self.run(lambda: self.hood.set(rotation))
    
    def hoodUpFF(self) -> Command:
        return self.run(lambda: self.hood.set(-0.8 + (-self.armFeedForward.calculate(0,self.hood.getEncoder().getVelocity()/12))))
    
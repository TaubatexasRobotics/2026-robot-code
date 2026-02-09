from rev import SparkMax, SparkLowLevel, ResetMode, PersistMode, SparkMaxConfig, SparkBaseConfig
from commands2 import Subsystem
from wpilib import SmartDashboard

class Shooter(Subsystem):
    def __init__(self, kS: int, kV: int, kA: int, setpoint: int) -> None:
        self.motor = SparkMax(11, SparkLowLevel.MotorType.kBrushless)

        config = SparkMaxConfig()

        config.smartCurrentLimit(40)
        config.setIdleMode(SparkBaseConfig.IdleMode.kCoast)

        config.closedLoop.pid(0, 0, 0)
        config.closedLoop.feedForward.kS(kS)
        config.closedLoop.feedForward.kV(kV)
        config.closedLoop.feedForward.kA(kA)
        
        self.motor.configure(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )

        #self.controller = self.motor.getClosedLoopController()
        #config.closedLoop.maxMotion.cruiseVelocity()
        #config.closedLoop.maxAcceleration.cruiseVelocity()
        #config.closedLoop.allowedProfileError.cruiseVelocity()

        #self.motor.setSetpoint(setpoint, SparkLowLevel.ControlType.kMAXMotionVelocityControl)
        SmartDashboard.putNumber("kS", 0.1)
        
    def periodic(self) -> None:
        self.setFeedforwardConstraints(
            SmartDashboard.getNumber("kS", 0),
            0,
            0
        )

    def setFeedforwardConstraints(self, kS: int, kV: int, kA: int) -> None:
        config = SparkMaxConfig()

        config.smartCurrentLimit(40)
        config.setIdleMode(SparkBaseConfig.IdleMode.kCoast)

        config.closedLoop.pid(0, 0, 0)
        config.closedLoop.feedForward.kS(kS)
        config.closedLoop.feedForward.kV(kV)
        config.closedLoop.feedForward.kA(kA)

        self.motor.configure(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )

    def activateShooter(self) -> None:
        self.motor.set(0.7)

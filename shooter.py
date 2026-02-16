from rev import (
    SparkMax,
    SparkLowLevel,
    ResetMode,
    PersistMode,
    SparkMaxConfig,
    SparkBaseConfig,
)
from commands2 import Subsystem, Command
from commands2.cmd import run
from wpilib import SmartDashboard
from wpimath.controller import BangBangController, SimpleMotorFeedforwardMeters, PIDController
from wpimath.units import rotationsPerMinuteToRadiansPerSecond
import constants


class Shooter(Subsystem):
    flywheel: SparkMax = SparkMax(constants.kFlywheelId, SparkLowLevel.MotorType.kBrushless)
    bangBangController: BangBangController = BangBangController()

    def __init__(self) -> None:
        config = SparkMaxConfig()

        config.smartCurrentLimit(40)
        config.setIdleMode(SparkBaseConfig.IdleMode.kCoast)
        config.closedLoop.feedForward.sva(*constants.kFlywheelFeedForward)
        config.closedLoop.pid(*constants.kFlywheelPID)

        self.feedforward = SimpleMotorFeedforwardMeters(*constants.kFlywheelFeedForward[:3])
        self.pid = PIDController(*constants.kFlywheelPID[:3])

        self.flywheel.configure(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )

        self.closedLoopController = self.flywheel.getClosedLoopController()

        self.encoder = self.flywheel.getEncoder()
        SmartDashboard.putData(self.bangBangController)

        SmartDashboard.putData("Shooter BangBang Controller", self.bangBangController)
        SmartDashboard.putNumberArray("Shooter PID Controller", [*constants.kFlywheelPID[:3]])
        SmartDashboard.putNumber("Shooter Setpoint", 0)
        SmartDashboard.putNumberArray("Shooter FeedForward", [*constants.kFlywheelFeedForward[:3]])

    def activate(self) -> None:
        self.flywheel.set(0.7)
    
    def periodic(self) -> None:
        feedforward = SmartDashboard.getNumberArray("Shooter FeedForward", [0, 0, 0])
        self.pid.setPID(*SmartDashboard.getNumberArray("Shooter PID Controller", [0, 0, 0]))
        self.feedforward.setKs(feedforward[0])
        self.feedforward.setKv(feedforward[1])
        self.feedforward.setKa(feedforward[2])

    def setFlywheelBySetpoint(self, setpoint: float) -> None:
        output = self.pid.calculate(self.encoder.getPosition(), setpoint)
        self.flywheel.set(output)
    
    def setFlywheelBySetpointCommand(self) -> Command:
        return run(lambda: self.setFlywheelBySetpoint(SmartDashboard.getNumber("Shooter Setpoint", 0)))

    def deactivate(self) -> None:
        self.flywheel.set(0)
    
    def bangBangActivate(self, maxSetpoint: float) -> None:
        setpoint = max(0, rotationsPerMinuteToRadiansPerSecond(maxSetpoint))
        output = self.bangBangController.calculate(self.encoder.getPosition(), setpoint) * 12.0
        self.closedLoopController.setReference(
            output + 0.9 * self.feedforward.calculate(setpoint), SparkMax.ControlType.kVoltage
        )
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
        self.flywheel_encoder = self.flywheel.getEncoder()
        self.bangBangController = BangBangController()
        self.hood = rev.SparkMax(53, rev.SparkMax.MotorType.kBrushless)
        self.hood_encoder = self.hood.getEncoder()

        self.hood_pid = wpimath.controller.PIDController(0.006, 0.0, 0.0)
        self.hood_pid.setTolerance(0.1)
        self.hood_encoder.setPosition(0)

        config = SparkMaxConfig()

        config.smartCurrentLimit(40)
        config.setIdleMode(SparkBaseConfig.IdleMode.kCoast)
        config.closedLoop.feedForward.sva(*constants.kFlywheelFeedForward)
        config.closedLoop.pid(*constants.kFlywheelPID)

        self.flywheel_feedforward = SimpleMotorFeedforwardMeters(
            *constants.kFlywheelFeedForward[:3]
        )
        self.flywheel_pid = PIDController(*constants.kFlywheelPID[:3])

        self.flywheel.configure(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )

        self.closedLoopController = self.flywheel.getClosedLoopController()

        SmartDashboard.putData(self.bangBangController)

        SmartDashboard.putData("Shooter BangBang Controller", self.bangBangController)
        SmartDashboard.putNumberArray(
            "Shooter PID Controller", [*constants.kFlywheelPID[:3]]
        )
        SmartDashboard.putNumber("Shooter Setpoint", 0)
        SmartDashboard.putNumberArray(
            "Shooter FeedForward", [*constants.kFlywheelFeedForward[:3]]
        )

    def activate(self) -> None:
        self.flywheel.set(0.7)

    def periodic(self) -> None:
        feedforward = SmartDashboard.getNumberArray("Shooter FeedForward", [0, 0, 0])
        self.pid.setPID(
            *SmartDashboard.getNumberArray("Shooter PID Controller", [0, 0, 0])
        )
        self.feedforward.setKs(feedforward[0])
        self.feedforward.setKv(feedforward[1])
        self.feedforward.setKa(feedforward[2])

        SmartDashboard.putData("PID", self.hood_pid)
        SmartDashboard.putNumber("crest encoder", self.hood_encoder.getPosition())
        SmartDashboard.putNumber("crest position", float(self.getPosition()))
        # self.pid.setSetpoint(self.setpoint)
        print(self.hood_pid.getSetpoint())

    def getPosition(self) -> float:
        return self.hood_encoder.getPosition() * gear_ratio * 360

    def move_to_setpoint(self):
        current_position = self.getPosition()
        hood_value = self.hood_pid.calculate(current_position)
        hood_value = Utils.clamp(hood_value, -0.4, 0.4)
        self.hood.set(hood_value)

    def move_to(self, setpoint):
        current_position = self.getPosition()
        hood_value = self.hood_pid.calculate(current_position, setpoint)
        hood_value = Utils.clamp(hood_value, -0.4, 0.4)
        self.hood.set(hood_value)

    def up(self):
        self.move_to(20)

    def down(self):
        self.move_to(0)

    def subir(self):
        self.hood.set(0.2)

    def descer(self):
        self.hood.set(-0.05)

    def stop(self):
        self.hood.stopMotor()

    def setFlywheelBySetpoint(self, setpoint: float) -> None:
        output = self.flywheel_pid.calculate(self.flywheel_encoder.getPosition(), setpoint)
        self.flywheel.set(output)

    def setFlywheelBySetpointCommand(self) -> Command:
        return run(
            lambda: self.setFlywheelBySetpoint(
                SmartDashboard.getNumber("Shooter Setpoint", 0)
            )
        )

    def deactivate(self) -> None:
        self.flywheel.set(0)

    def bangBangActivate(self, maxSetpoint: float) -> None:
        setpoint = max(0, rotationsPerMinuteToRadiansPerSecond(maxSetpoint))
        output = (
            self.bangBangController.calculate(self.flywheel_encoder.getPosition(), setpoint)
            * 12.0
        )
        self.closedLoopController.setReference(
            output + 0.9 * self.flywheel_feedforward.calculate(setpoint),
            SparkMax.ControlType.kVoltage,
        )

from phoenix5 import WPI_VictorSPX, ControlMode
from commands2 import Command, Subsystem
from commands2.cmd import run


class Climber(Subsystem):
    def __init__(self) -> None:
        self.climber = WPI_VictorSPX(1)
        self.setDefaultCommand(run(lambda: self.stop()))

    def clockwise(self) -> None:
        self.climber.set(ControlMode.PercentOutput, 1)

    def stop(self) -> None:
        self.climber.set(ControlMode.PercentOutput, 0)

    def counterclockwise(self) -> None:
        self.climber.set(ControlMode.PercentOutput, -1)

    def up(self) -> Command:
        return run(lambda: self.clockwise())

    def down(self) -> Command:
        return run(lambda: self.counterclockwise())

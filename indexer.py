from commands2 import Command, Subsystem
from phoenix5 import WPI_VictorSPX, ControlMode
import constants
from typing import Callable

class Indexer(Subsystem):
    def __init__(self) -> None:
        self.front_roller = WPI_VictorSPX(constants.kFrontRoller)
        self.back_roller = WPI_VictorSPX(constants.kBackRoller)

    def feed(self, front_perc, back_perc) -> None:
        self.front_roller.set(ControlMode.PercentOutput, front_perc)
        self.back_roller.set(ControlMode.PercentOutput, back_perc)
    
    def feedAxis(self, axis: Callable[[], float]) -> Command:
        return self.run(lambda: self.feed(axis() * -0.35, axis() * -0.8))

    def feedAxisInverted(self, axis: Callable[[], float]) -> Command:
        return self.run(lambda: self.feed(axis() * 0.35, axis() * -0.8))

    def activateFeed(self) -> Command:
        return self.run(lambda: self.feed(-0.35, -0.8))
    
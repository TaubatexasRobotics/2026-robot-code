from commands2 import ParallelCommandGroup
from commands2.cmd import run
from phoenix5 import WPI_VictorSPX
import constants

class Indexer:
    def __init__(self) -> None:
        self.front_roller = WPI_VictorSPX(constants.kFrontRoller)
        self.back_roller = WPI_VictorSPX(constants.kBackRoller)

    def feed(self) -> Command:
        return ParallelCommandGroup(
            run(lambda: self.front_roller.set(-0.5)),
            run(lambda: self.back_roller.set(1))
        )

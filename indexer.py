from commands2 import ParallelCommandGroup
from commands2.cmd import run
from phoenix5 import WPI_VictorSPX

class Indexer:
    def __init__(self) -> None:
        self.front_roller = WPI_VictorSPX(7)
        self.back_roller = WPI_VictorSPX(8)

    def feed(self) -> Command:
        return ParallelCommandGroup(
            run(lambda: self.front_roller.set(-1)),
            run(lambda: self.back_roller.set(1))
        )

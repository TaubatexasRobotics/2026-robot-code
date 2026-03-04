from commands2 import ParallelCommandGroup, Subsystem
from phoenix5 import WPI_VictorSPX
import constants

class Indexer(Subsystem):
    def __init__(self) -> None:
        self.front_roller = WPI_VictorSPX(constants.kFrontRoller)
        self.back_roller = WPI_VictorSPX(constants.kBackRoller)

        self.setDefaultCommand(
            self.run(lambda: self.deactivate())    
        )

    def feed(self) -> None:
        self.front_roller.set(-0.5)
        self.back_roller.set(-0.7)
    
    def deactivate(self) -> None:
        self.front_roller.set(0)
        self.back_roller.set(0)
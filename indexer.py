from commands2 import Command, Subsystem
from phoenix5 import WPI_VictorSPX, ControlMode
import constants

class Indexer(Subsystem):
    def __init__(self) -> None:
        self.front_roller = WPI_VictorSPX(constants.kFrontRoller)
        self.back_roller = WPI_VictorSPX(constants.kBackRoller)

        self.setDefaultCommand(self.run(lambda: self.stop()))

    def stop(self) -> None:
        self.front_roller.set(ControlMode.PercentOutput, 0)
        self.back_roller.set(ControlMode.PercentOutput, 0)

    def feed(self) -> None:
        self.front_roller.set(ControlMode.PercentOutput, -0.1)
        self.back_roller.set(ControlMode.PercentOutput, -0.8)
    
    def expulse(self) -> None:
        self.front_roller.set(ControlMode.PercentOutput, -0.1)
        self.back_roller.set(ControlMode.PercentOutput, 0.4)
    
    def activateFeed(self) -> Command:
        return self.run(lambda: self.feed())

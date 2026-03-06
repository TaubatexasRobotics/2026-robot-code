from phoenix5 import WPI_VictorSPX, ControlMode
from commands2 import Subsystem, Command
from wpilib import Timer, SmartDashboard
import constants


class Intake(Subsystem):
    def __init__(self) -> None:
        self.pivot = WPI_VictorSPX(constants.kIntakeAngleId)
        self.roller = WPI_VictorSPX(constants.kIntakeTrackId)
        self.pivotUp = False
        self.lastBurstTime = 0.0

        SmartDashboard.putNumber("up", 0.5)
        SmartDashboard.putNumber("down", 0.9)

        SmartDashboard.putBoolean("pivotUp", self.pivotUp)
        self.pivot.setInverted(True)
        self.setDefaultCommand(self.stopGamePieceCollector())

    def isPivotUp(self) -> bool:
        return self.pivotUp

    def periodic(self) -> None:
        elapsed = Timer.getFPGATimestamp() - self.lastBurstTime
        percent = 0

        SmartDashboard.putBoolean("pivotUp", self.pivotUp)
        kPivotTimeUp = SmartDashboard.getNumber("up", 0)
        kPivotTimeDown = SmartDashboard.getNumber("down", 0)

        if self.pivotUp:
            percent = 0.5 if elapsed < kPivotTimeUp else 0
        else:
            percent = -0.7 if elapsed < kPivotTimeDown else 0

        self.pivot.set(ControlMode.PercentOutput, percent)

    def startPivotUp(self) -> None:
        if self.pivotUp:
            return

        self.pivotUp = True
        self.lastBurstTime = Timer.getFPGATimestamp()

    def stopPivot(self) -> None:
        self.pivot.set(0)

    def startPivotDown(self) -> None:
        if not self.pivotUp:
            return

        self.pivotUp = False
        self.lastBurstTime = Timer.getFPGATimestamp()

    def up(self) -> Command:
        return self.run(lambda: self.startPivotUp())

    def down(self) -> Command:
        return self.run(lambda: self.startPivotDown())

    def releaseGamePiece(self) -> Command:
        return self.run(lambda: self.roller.set(ControlMode.PercentOutput, -1))

    def stopGamePieceCollector(self) -> Command:
        return self.run(lambda: self.roller.set(ControlMode.PercentOutput, 0))

    def colectGamePiece(self) -> Command:
        return self.run(lambda: self.roller.set(ControlMode.PercentOutput, 1))
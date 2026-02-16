from phoenix5 import WPI_VictorSPX, ControlMode
from commands2 import Subsystem, Command
from wpilib import Timer, SmartDashboard
import constants


class Intake(Subsystem):
    pivot: WPI_VictorSPX = WPI_VictorSPX(constants.kIntakeAngleMotor)
    roller: WPI_VictorSPX = WPI_VictorSPX(constants.kIntakeTrackMotor)
    pivotUp: bool = False
    lastBurstTime: int = 0

    def __init__(self) -> None:
        kPivotTimeUp = SmartDashboard.putNumber("up", 0.5)
        kPivotTimeDown = SmartDashboard.putNumber("down", 0.5)
        self.pivot.setInverted(True)

    def isPivotUp(self) -> bool:
        return self.pivotUp

    def periodic(self) -> None:
        elapsed = Timer.getFPGATimestamp() - self.lastBurstTime
        percent = 0

        kPivotTimeUp = SmartDashboard.getNumber("up", 0)
        kPivotTimeDown = SmartDashboard.getNumber("down", 0)
        
        if self.pivotUp:
            percent = 1 if elapsed < kPivotTimeUp else 0
        else:
            percent = -1 if elapsed < kPivotTimeDown else 0
        
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

    def collectGamePiece(self) -> None:
        self.roller.set(ControlMode.PercentOutput, -1)

    def stopGamePieceCollector(self) -> None:
        self.roller.set(ControlMode.PercentOutput, 0)

    def releaseGamePiece(self) -> None:
        self.roller.set(ControlMode.PercentOutput, 1)
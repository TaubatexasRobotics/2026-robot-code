from phoenix5 import WPI_VictorSPX, ControlMode
from commands2 import Subsystem
from wpilib import Timer, SmartDashboard
import constants


class Intake(Subsystem):
    def __init__(self) -> None:
        self.pivot = WPI_VictorSPX(constants.kIntakeAngleMotor)
        self.roller = WPI_VictorSPX(constants.kIntakeTrackMotor)
        self.pivotUp = False
        self.lastBurstTime = 0

        kPivotTimeUp = SmartDashboard.putNumber("up", 0.5)
        kPivotTimeDown = SmartDashboard.putNumber("down", 0.5)

    def isPivotUp(self) -> bool:
        return self.pivotUp

    def periodic(self) -> None:
        elapsed = Timer.getFPGATimestamp() - self.lastBurstTime
        percent = 0

        kPivotTimeUp = SmartDashboard.getNumber("up", 0)
        kPivotTimeDown = SmartDashboard.getNumber("down", 0)
        
        if self.pivotUp:
            percent = -1 if elapsed < kPivotTimeUp else 0
        else:
            percent = 1 if elapsed < kPivotTimeDown else 0
        
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

    def get(self) -> None:
        self.roller.set(-1)

    def stop(self) -> None:
        self.roller.set(0)

    def release(self) -> None:
        self.roller.set(1)
from phoenix5 import WPI_VictorSPX, ControlMode
from rev import SparkMax, SparkLowLevel
from commands2 import Subsystem, Command
from wpilib import Timer, SmartDashboard
import constants
from phoenix6 import signals
from phoenix6.hardware import TalonFX
from phoenix6.controls import DutyCycleOut   
from wpimath.controller import PIDController

UP_PIVOT_SPEED = -0.7
DOWN_PIVOT_SPEED = 0.5
RELEASE_INTAKE_SPEED = -0.6
COLLECT_INTAKE_SPEED = 0.4

class Intake(Subsystem):
    def __init__(self) -> None:
        # Motors definition
        self.pivot = SparkMax(constants.Kintake_pivot_id, SparkLowLevel.MotorType.kBrushless)
        self.roller = TalonFX(constants.Kintake_roller_id)
        
        # Encoders definition
        self.pivot_encoder = self.pivot.getEncoder()
        self.pivot_encoder.setPosition(0)
        self.roller.set_position(0)

        # Some definitions
        self.pivotUp = False
        self.lastBurstTime = 0.0
        self.setDefaultCommand(self.stopGamePieceCollector())
        self.pivot_PID = PIDController(*constants.Kpivot_PID)

        #TODO: virtual endstop
        # self.pivot.getOutputCurrent()

    def isPivotUp(self) -> bool:
        return self.pivotUp

    def periodic(self) -> None:
        elapsed = Timer.getFPGATimestamp() - self.lastBurstTime
        percent = 0

        kPivotTimeUp = 1.2
        kPivotTimeDown = 0.5

        if self.pivotUp:
            percent = DOWN_PIVOT_SPEED if elapsed < kPivotTimeUp else 0
        else:
            percent = UP_PIVOT_SPEED if elapsed < kPivotTimeDown else 0

        self.pivot.set(percent)

        # SmartDashboard
        SmartDashboard.putNumber("Intake/Pivot Position in Degrees", self.pivot_encoder.getPosition() * 360)
        SmartDashboard.putNumber("Intake/Pivot Velocity", self.pivot_encoder.getVelocity())
        SmartDashboard.putNumber("Intake/Roller Position in Degrees", self.roller.get_position().value / 45.52)
        SmartDashboard.putNumber("Intake/Roller Velocity", self.roller.get_acceleration().value)
    
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

    def getAboveCurrent(self, current):
        return self.pivot.getOutputCurrent() > current
        
    def downPivotByCurrent(self) -> Command:
        return self.run(lambda: self.pivot.set(-0.8)).until(lambda: self.getAboveCurrent(20))
        
    def upPivotByCurrent(self) -> Command:
        return self.run(lambda: self.pivot.set(0.8)).until(lambda: self.getAboveCurrent(20))
    
    def UpByEncoder(self) -> Command:
        output = self.pivot_PID.calculate(self.pivot_encoder.getPosition() * 360, 20)
        return self.run(lambda: self.pivot.set(output))
    
    def setPivotDownByEncoder(self):
        output = self.pivot_PID.calculate(self.pivot_encoder.getPosition() * 360, 0)
        self.pivot.set(output)

    def DownByEncoder(self) -> Command:
        return self.run(self.setPivotDownByEncoder)

    def upWithTime(self) -> Command:
        return self.run(lambda: self.startPivotUp())

    def downWithTime(self) -> Command:
        return self.run(lambda: self.startPivotDown())
    
    def releaseGamePiece(self) -> Command:
        return self.run(lambda: self.roller.set(RELEASE_INTAKE_SPEED))

    def stopGamePieceCollector(self) -> Command:
       return self.run(lambda: self.roller.set(0))

    def colectGamePiece(self) -> Command:
        return self.run(lambda: self.roller.set(COLLECT_INTAKE_SPEED))
    
    def up(self) -> Command:
        return self.run(lambda: self.pivot.set(UP_PIVOT_SPEED))
    
    def down(self) -> Command:
        return self.run(lambda: self.pivot.set(DOWN_PIVOT_SPEED))
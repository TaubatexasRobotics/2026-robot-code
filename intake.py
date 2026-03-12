from phoenix5 import WPI_VictorSPX, ControlMode
from rev import SparkMax, SparkLowLevel
from commands2 import Subsystem, Command
from wpilib import Timer, SmartDashboard
import constants
from phoenix6 import signals
from phoenix6.hardware import TalonFX
from phoenix6.controls import DutyCycleOut   
from wpimath.controller import PIDController


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

        #TODO: virtual endstop
        # self.pivot.getOutputCurrent()

    # def get_velocity(self):
    #     distance = self.roller.get_position
    #     time =

    # def isPivotUp(self) -> bool:
    #     return self.pivotUp

    def periodic(self) -> None:
        elapsed = Timer.getFPGATimestamp() - self.lastBurstTime
        percent = 0

        kPivotTimeUp = 1.2
        kPivotTimeDown = 0.5

        if self.pivotUp:
            percent = 0.5 if elapsed < kPivotTimeUp else 0
        else:
            percent = -0.7 if elapsed < kPivotTimeDown else 0

        self.pivot.set(ControlMode.PercentOutput, percent)

        # SmartDashboard
        SmartDashboard.putNumber("Intake/Pivot Position in Degrees", self.pivot_encoder.getPosition() * 360)
        SmartDashboard.putNumber("Intake/Pivot Velocity", self.pivot_encoder.getVelocity())
        SmartDashboard.putNumber("Intake/Roller Position in Degrees", self.roller.get_position() / 45.52)
        SmartDashboard.putNumber("Intake/Roller Velocity", self.roller.get_acceleration())
    
    '''
    # def startPivotUp(self) -> None:
    #     if self.pivotUp:
    #         return

    #     self.pivotUp = True
    #     self.lastBurstTime = Timer.getFPGATimestamp()

    # def stopPivot(self) -> None:
    #     self.pivot.set(0)

    # def startPivotDown(self) -> None:
    #     if not self.pivotUp:
    #         return

    #     self.pivotUp = False
    #     self.lastBurstTime = Timer.getFPGATimestamp()
    '''

    def UpByEncoder(self) -> Command:
        output = constants.Kintake_PID.calculate(self.pivot_encoder.getPosition() * 360, 20)
        return self.run(lambda: self.pivot.set(output))
    
    def setPivotDownByEncoder(self):
        output = constants.Kintake_PID.calculate(self.pivot_encoder.getPosition() * 360, 0)
        self.pivot.set(output)

    def DownByEncoder(self) -> Command:
        return self.run(self.setPivotDownByEncoder)

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
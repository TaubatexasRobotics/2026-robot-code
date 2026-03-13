from commands2 import Subsystem, Command, sequentialcommandgroup, PIDCommand
from phoenix5 import WPI_VictorSPX
from navx import AHRS
from typing import Callable
import constants
from wpilib.drive import DifferentialDrive
from wpilib import MotorControllerGroup, Field2d, SmartDashboard
from wpimath.controller import PIDController

class Drivetrain(Subsystem):

    def __init__(self):
        # Motors definition
        self.left_front_motor = WPI_VictorSPX(constants.Kleft_front_id)
        self.left_back_motor = WPI_VictorSPX(constants.Kleft_back_id)
        self.right_front_motor = WPI_VictorSPX(constants.Kright_front_id)
        self.right_back_motor = WPI_VictorSPX(constants.Kright_back_id)

        # Motors agroup and DifferentialDrive definition
        self.left_motors = MotorControllerGroup(self.left_front_motor, self.left_back_motor) # Left
        self.right_motors = MotorControllerGroup(self.right_front_motor, self.right_back_motor) # Right
        self.right_motors.setInverted(True)
        
        self.drivetrain = DifferentialDrive(self.left_motors, self.right_motors)

        # Navx
        self.navx = AHRS.create_spi()

        # Configs
        self.drivetrain.setSafetyEnabled(True)
        self.drivetrain.setExpiration(0.1)
        self.drivetrain.setMaxOutput(1.0)

        self.field = Field2d()
        self.slowMode = False
        

    def periodic(self):
        # SmartDashboard
        SmartDashboard.putNumber("Drivetrain/Left Front Motor", self.left_front_motor.get())
        SmartDashboard.putNumber("Drivetrain/Left Back Motor", self.left_back_motor.get())
        SmartDashboard.putNumber("Drivetrain/Right Front Motor", self.right_front_motor.get())
        SmartDashboard.putNumber("Drivetrain/Right Back Motor", self.right_back_motor.get())

    def setSlowMode(self) -> Command:
        return self.run(lambda: setattr(self, "slowMode", not self.slowMode))

    def arcadeDriveCommand(self, speed: Callable[[], float], rotate: Callable[[], float]) -> Command:
        if self.slowMode:
            return self.run(lambda: self.drivetrain.arcadeDrive(speed() * 0.5, rotate() * 0.5))
        return self.run(lambda: self.drivetrain.arcadeDrive(speed(), rotate(), False))
    
    def cheesyDrive(self,speed: Callable[[], float],rotate: Callable[[], float], allowTurnInPlace: bool,) -> Command:
        return self.run(lambda: self.drivetrain.curvatureDrive(speed(), rotate(), allowTurnInPlace))

    def tankDrive(self, left_speed: Callable[[], float], right_speed: Callable[[], float]) -> Command:
        return self.run(lambda: self.drivetrain.tankDrive(left_speed(), right_speed()))
    
    def rotate(self, angle: float) -> Command:
        return PIDCommand(
            PIDController(*constants.Kdrivetrain_PID),
            lambda: self.navx.getAngle(),
            angle,
            lambda output: self.drivetrain.arcadeDrive(0, output, False),
            self,
        )

    def front(self) -> Command:
        return self.run(lambda: self.drivetrain.arcadeDrive(0.9, 0, False))
    
    def back(self) -> Command:
        return self.run(lambda: self.drivetrain.arcadeDrive(-0.9, 0, False))
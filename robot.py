import constants
from drivetrain import Drivetrain
from genericjoystick import GenericJoystick
from autonomous.basicauto import BasicAuto
from commands2 import TimedCommandRobot, CommandScheduler, Command
from typing import Optional
from commands2.cmd import run
from camera import Camera, PhotonVisionCamera, LimelightCamera
from turret import Turret
from commands2.button import JoystickButton
from intake import Intake
from pathplannerlib.auto import AutoBuilder
from wpilib import SmartDashboard, SendableChooser
from wpilib.interfaces import GenericHID


class Robot(TimedCommandRobot):
    autonomous: Optional[Command] = None
    drivetrain: Drivetrain = Drivetrain()
    intake: Intake = Intake()
    autoChooser: SendableChooser = AutoBuilder.buildAutoChooser()
    driverJoystick: GenericHID = GenericJoystick(constants.kJoystickDriverPort)

    def robotInit(self) -> None:
        self.autoChooser.addOption("Basic Auto", BasicAuto(self.drivetrain))
        
        JoystickButton(self.driverJoystick, 1).onTrue(
            run(
                lambda: self.intake.startPivotUp(),
                self.intake
            )
        )

        JoystickButton(self.driverJoystick, 2).onTrue(
            run(
                lambda: self.intake.startPivotDown(),
                self.intake
            )
        )

        self.drivetrain.setDefaultCommand(
            self.drivetrain.arcadeDrive(
                self.driverJoystick.getLeftYAxis(),
                self.driverJoystick.getRightXAxis(),
            )
        )
        
    def autonomousInit(self) -> None:
        self.autonomous = self.autoChooser.getSelected()
        self.autonomous.schedule()

    def autonomousExit(self) -> None:
        CommandScheduler.getInstance().cancelAll()
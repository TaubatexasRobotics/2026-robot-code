import constants
from drivetrain import Drivetrain
from autonomous.autoltvcontroller import AutoLTVController
from autonomous.drivestraightpath import DriveStraightPath
from commands2 import TimedCommandRobot, CommandScheduler, Command, ParallelCommandGroup
from typing import Optional
from commands2.button import JoystickButton
from intake import Intake
from pathplannerlib.auto import AutoBuilder
from wpilib import SmartDashboard, SendableChooser, DriverStation, Joystick
from commands2.sysid import SysIdRoutine
from shooter import Shooter
from turret import Turret
from camera import Pixy2, LimelightCamera, PhotonVisionCamera
from indexer import Indexer

class Robot(TimedCommandRobot):
    autonomous: Optional[Command] = None
    
    drivetrain: Drivetrain = Drivetrain()
    intake: Intake = Intake()
    autoChooser: SendableChooser = AutoBuilder.buildAutoChooser()
    driverJoystick: Joystick = Joystick(constants.kJoystickDriverPort)
    shooter: Shooter = Shooter()
    turret: Turret = Turret()
    indexer: Indexer = Indexer()

    def robotInit(self) -> None:
        JoystickButton(self.driverJoystick, 1).whileTrue(
            ParallelCommandGroup(
                self.shooter.activateFlywheel(),
                self.indexer.feed()
            )
        )

        JoystickButton(self.driverJoystick, 7).whileTrue(self.intake.up())
        JoystickButton(self.driverJoystick, 8).whileTrue(self.intake.down())
        
        self.autoChooser.addOption(
            "LTV Controller Test Auto", AutoLTVController(self.drivetrain)
        )
        self.autoChooser.addOption(
            "Drive Straight Path", DriveStraightPath(self.drivetrain, 5)
        )
        SmartDashboard.putData("Auto Chooser", self.autoChooser)

    def autonomousInit(self) -> None:
        DriverStation.silenceJoystickConnectionWarning(True)
        self.autonomous = self.autoChooser.getSelected()

        if self.autonomous:
            self.autonomous.schedule()

    def autonomousPeriodic(self) -> None:
        pass

    def autonomousExit(self) -> None:
        CommandScheduler.getInstance().cancelAll()
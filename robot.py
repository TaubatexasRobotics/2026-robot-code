import constants
from drivetrain import Drivetrain
from genericjoystick import GenericJoystick
from autonomous.autoltvcontroller import AutoLTVController
from autonomous.drivestraightpath import DriveStraightPath
from commands2 import TimedCommandRobot, CommandScheduler, Command
from typing import Optional
from commands2.button import JoystickButton
from intake import Intake
from pathplannerlib.auto import AutoBuilder
from wpilib import SmartDashboard, SendableChooser, DriverStation
from commands2.sysid import SysIdRoutine
from shooter import Shooter
from camera import PixyFuelDetector, LimelightCamera, PhotonVisionCamera

class Robot(TimedCommandRobot):
    autonomous: Optional[Command] = None

    def robotInit(self) -> None:
        self.drivetrain = Drivetrain()
        self.intake = Intake()
        self.autoChooser = AutoBuilder.buildAutoChooser()
        self.driverJoystick = GenericJoystick(constants.kJoystickDriverPort)
        self.shooter = Shooter()

        self.pixy: PixyFuelDetector = PixyFuelDetector()

        self.autoChooser.addOption(
            "LTV Controller Test Auto", AutoLTVController(self.drivetrain)
        )
        self.autoChooser.addOption(
            "Drive Straight Path", DriveStraightPath(self.drivetrain, 5)
        )
        SmartDashboard.putData("Auto Chooser", self.autoChooser)

    def teleopInit(self) -> None:
        JoystickButton(self.driverJoystick, 5).onTrue(self.intake.up())

        JoystickButton(self.driverJoystick, 6).onTrue(self.intake.down())

        JoystickButton(self.driverJoystick, 1).onTrue(
            self.drivetrain.sysIdQuasistatic(SysIdRoutine.Direction.kReverse)
        )

        JoystickButton(self.driverJoystick, 2).onTrue(
            self.drivetrain.sysIdQuasistatic(SysIdRoutine.Direction.kForward)
        )

        JoystickButton(self.driverJoystick, 3).onTrue(
            self.drivetrain.sysIdDynamic(SysIdRoutine.Direction.kForward)
        )

        JoystickButton(self.driverJoystick, 4).onTrue(
            self.drivetrain.sysIdDynamic(SysIdRoutine.Direction.kReverse)
        )

        self.drivetrain.setDefaultCommand(
            self.drivetrain.arcadeDrive(
                lambda: self.driverJoystick.getLeftYAxis(),
                lambda: self.driverJoystick.getRightXAxis(),
            )
        )

    def autonomousInit(self) -> None:
        DriverStation.silenceJoystickConnectionWarning(True)
        self.autonomous = self.autoChooser.getSelected()

        if self.autonomous:
            self.autonomous.schedule()

    def autonomousPeriodic(self) -> None:
        pass

    def autonomousExit(self) -> None:
        CommandScheduler.getInstance().cancelAll()

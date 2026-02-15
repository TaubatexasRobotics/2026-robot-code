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
from commands2.sysid import SysIdRoutine


class Robot(TimedCommandRobot):
    autonomous: Optional[Command] = None
    drivetrain: Drivetrain = Drivetrain()
    intake: Intake = Intake()
    autoChooser: SendableChooser = AutoBuilder.buildAutoChooser()
    driverJoystick: GenericHID = GenericJoystick(constants.kJoystickDriverPort)

    def robotInit(self) -> None:
        self.autoChooser.addOption("Basic Auto", BasicAuto(self.drivetrain))
        SmartDashboard.putData("Auto Chooser", self.autoChooser)
        
        JoystickButton(self.driverJoystick, 5).onTrue(
            run(
                lambda: self.intake.startPivotUp(),
                self.intake
            )
        )

        JoystickButton(self.driverJoystick, 6).onTrue(
            run(
                lambda: self.intake.startPivotDown(),
                self.intake
            )
        )

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
        self.autonomous = self.autoChooser.getSelected()
        self.autonomous.schedule()

    def autonomousExit(self) -> None:
        CommandScheduler.getInstance().cancelAll()

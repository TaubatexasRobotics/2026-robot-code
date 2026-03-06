import constants
from drivetrain import Drivetrain
from autonomous.drivestraightpath import DriveStraightPath
from commands2 import TimedCommandRobot, CommandScheduler, Command, ParallelCommandGroup, SequentialCommandGroup
from typing import Optional
from led import LEDController
from commands2.button import JoystickButton, POVButton
from intake import Intake
from wpilib import SmartDashboard, SendableChooser, DriverStation, Joystick
from shooter import Shooter
from turret import Turret
from camera import PhotonVisionCamera
from indexer import Indexer
from commands2.cmd import run

class Robot(TimedCommandRobot):
    autonomous: Optional[Command] = None
    autoChooser: SendableChooser = SendableChooser()
    
    drivetrain: Drivetrain = Drivetrain()
    intake: Intake = Intake()
    driverJoystick: Joystick = Joystick(constants.kJoystickDriverPort)
    shooter: Shooter = Shooter()
    turret: Turret = Turret()
    indexer: Indexer = Indexer()
    led: LEDController = LEDController()
    turretCamera: PhotonVisionCamera = PhotonVisionCamera(constants.kCameraName)

    def combineAxis(self) -> float:
        leftTrigger = -self.driverJoystick.getRawAxis(2)
        rightTrigger = self.driverJoystick.getRawAxis(3)

        return rightTrigger + leftTrigger

    def robotInit(self) -> None:
        self.led.rainbow().schedule()

        JoystickButton(self.driverJoystick, 5).whileTrue(
            ParallelCommandGroup(
                self.indexer.activateFeed(),
                self.shooter.activateFlywheel(),
                self.intake.releaseGamePiece(),
                self.led.blue()
            )
        )
        
        JoystickButton(self.driverJoystick, 1).onTrue(self.drivetrain.setSlowMode())

        JoystickButton(self.driverJoystick, 2).whileTrue(
            self.indexer.activateExpulse()
        )
        
        JoystickButton(self.driverJoystick, 6).whileTrue(
            self.turret.followYawTag(self.turretCamera, self.led)
        )

        JoystickButton(self.driverJoystick, 7).whileTrue(
            self.shooter.hoodUpFF()
        )

        JoystickButton(self.driverJoystick, 8).whileTrue(
            self.shooter.hoodDown()
        )

        POVButton(self.driverJoystick, 90).whileTrue(
            self.intake.up()
        )

        POVButton(self.driverJoystick, 270).whileTrue(
            self.intake.down()
        )

        self.turret.setDefaultCommand(
            self.turret.activateYaw(lambda: self.driverJoystick.getRawAxis(4))
        )        

        self.drivetrain.setDefaultCommand(
            self.drivetrain.arcadeDrive(
                lambda: -self.combineAxis(),
                lambda: self.driverJoystick.getRawAxis(0)
            )
        )

        self.autoChooser.addOption(
            "Drive Straight Path", DriveStraightPath(self.drivetrain, 5)
        )
        SmartDashboard.putData("Auto Chooser", self.autoChooser)

    def teleopExit(self) -> None:
        self.led.blinkGreen().schedule()

    def autonomousInit(self) -> None:
        DriverStation.silenceJoystickConnectionWarning(True)
        self.autonomous = self.autoChooser.getSelected()

        if self.autonomous:
            self.autonomous.schedule()

    def autonomousPeriodic(self) -> None:
        pass

    def autonomousExit(self) -> None:
        CommandScheduler.getInstance().cancelAll()
import constants
from drivetrain import Drivetrain
from autonomous.drivestraightpath import DriveStraightPath
from commands2 import TimedCommandRobot, CommandScheduler, Command, ParallelCommandGroup, SequentialCommandGroup
from typing import Optional
from led import LEDController
from commands2.button import JoystickButton, POVButton, Trigger
from intake import Intake
from wpilib import SmartDashboard, SendableChooser, DriverStation, Joystick
from shooter import Shooter
from turret import Turret
from camera import PhotonVisionCamera
from indexer import Indexer

class Robot(TimedCommandRobot):
    autonomous: Optional[Command] = None
    autoChooser: SendableChooser = SendableChooser()
    
    drivetrain: Drivetrain = Drivetrain()
    intake: Intake = Intake()
    driverJoystick: Joystick = Joystick(constants.kJoystickDriverPort)
    copilotJoystick: Joystick = Joystick(constants.kJoystickCoDriverPort)
    shooter: Shooter = Shooter()
    turret: Turret = Turret()
    indexer: Indexer = Indexer()
    led: LEDController = LEDController()
    turretCamera: PhotonVisionCamera = PhotonVisionCamera(constants.kCameraName)

    def combineAxis(self, joystick: Joystick, left_axis, right_axis) -> float:
        leftTrigger = -joystick.getRawAxis(left_axis)
        rightTrigger = joystick.getRawAxis(right_axis)

        return rightTrigger + leftTrigger

    def robotInit(self) -> None:
        self.led.rainbow().schedule()

        #Driver Joystick
        POVButton(self.driverJoystick, 0).whileTrue(
            self.intake.up()
        )

        POVButton(self.driverJoystick, 180).whileTrue(
            self.intake.down()
        )

        JoystickButton(self.driverJoystick, 3).toggleOnTrue(self.intake.colectGamePiece())

        JoystickButton(self.driverJoystick, 4).whileTrue(self.intake.releaseGamePiece())
        
        self.drivetrain.setDefaultCommand(
            self.drivetrain.arcadeDrive(
                lambda: -self.combineAxis(self.driverJoystick, 2, 3),
                lambda: self.driverJoystick.getRawAxis(0)
            )
        )

        #Copilot Joystick
        JoystickButton(self.copilotJoystick, 6).toggleOnTrue(
            ParallelCommandGroup(
                self.shooter.activateFlywheel(),
                self.led.blue()
            )
        )

        self.turret.setDefaultCommand(
            self.turret.activateYaw(lambda: self.copilotJoystick.getRawAxis(0))
        )

        Trigger(lambda: self.copilotJoystick.getRawAxis(3) > 0.5).whileTrue(self.indexer.activateFeed())
        Trigger(lambda: self.copilotJoystick.getRawAxis(2) > 0.5).whileTrue(self.indexer.activateInvertedFeed())

        JoystickButton(self.copilotJoystick, 1).whileTrue(
            self.turret.followYawTag(self.turretCamera, self.led)
        )

        POVButton(self.copilotJoystick, 90).toggleOnTrue(
            self.shooter.hoodUp()
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

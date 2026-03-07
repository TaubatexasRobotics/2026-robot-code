import time
import constants
from drivetrain import Drivetrain
# from autonomous.drivestraightpath import DriveStraightPath
from commands2 import TimedCommandRobot, CommandScheduler, Command, ParallelCommandGroup, SequentialCommandGroup
from typing import Optional
from led import LEDController
from commands2.button import JoystickButton, POVButton
from intake import Intake
from wpilib import SmartDashboard, SendableChooser, DriverStation, Joystick, Timer
from shooter import Shooter
from turret import Turret
from camera import PhotonVisionCamera
from indexer import Indexer
from wpilib import SmartDashboard

class Robot(TimedCommandRobot):
    autonomous: Optional[Command] = None
    autoChooser: SendableChooser = SendableChooser()
    drivetrain: Drivetrain = Drivetrain()
    intake: Intake = Intake()
    driverJoystick: Joystick = Joystick(constants.kJoystickDriverPort)
    copilotJoystick : Joystick = Joystick(constants.kJoystickCoDriverPort)
    shooter: Shooter = Shooter()
    turret: Turret = Turret()
    indexer: Indexer = Indexer()
    led: LEDController = LEDController()
    timer: Timer = Timer()
    turretCamera: PhotonVisionCamera = PhotonVisionCamera(constants.kCameraName)
    

    def combineAxis(self, joystick: Joystick, left_axis, right_axis) -> float:
        leftTrigger = -joystick.getRawAxis(left_axis)
        rightTrigger = joystick.getRawAxis(right_axis)

        return rightTrigger + leftTrigger

    def robotInit(self) -> None:
        self.autoChooser = SendableChooser()

        self.autoChooser.addOption("Esquerda", "left")
        self.autoChooser.setDefaultOption("Centro", "center")
        self.autoChooser.addOption("Direita", "right")
        self.autoChooser.addOption("Desabilitado", "disabled")

        SmartDashboard.putData("Auto Position", self.autoChooser)
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

        self.indexer.setDefaultCommand(
             self.indexer.feedAxis(lambda: self.combineAxis(self.copilotJoystick, 2, 3))
        )

        self.turret.setDefaultCommand(
            self.turret.activateYaw(lambda: self.copilotJoystick.getRawAxis(0))
        )  
          
        # JoystickButton(self.copilotJoystick, 1).whileTrue(
            #     self.turret.followYawTag(self.turretCamera, self.led)
            # )
    

        POVButton(self.copilotJoystick, 180).toggleOnTrue(
            self.shooter.activateFlywheel100()
        )
        POVButton(self.copilotJoystick, 270).toggleOnTrue(
            self.shooter.activateFlywheel75()
        )
        POVButton(self.copilotJoystick, 0).toggleOnTrue(
            self.shooter.activateFlywheel50()
        )

        POVButton(self.copilotJoystick, 90).toggleOnTrue(
            self.shooter.hoodUp()
        )

        # self.autoChooser.addOption(
        #     "Drive Straight Path", DriveStraightPath(self.drivetrain, 5)
        # )
        # SmartDashboard.putData("Auto Chooser", self.autoChooser)

    def teleopExit(self) -> None:
        self.led.blinkGreen().schedule()
    
    def robotPeriodic(self):
        SmartDashboard.putNumber("Shooter velocity", self.shooter.flywheel.getEncoder().getVelocity())
        SmartDashboard.putNumber("Shooter power", self.shooter.flywheel.get())
        SmartDashboard.putNumber("Drivetrain/Left encoder", self.drivetrain.left_encoder.getPosition())
        SmartDashboard.putNumber("Drivetrain/Right encoder", self.drivetrain.right_encoder.getPosition())

    def autonomousInit(self) -> None:
        self.drivetrain.resetEncoders()
        self.timer.reset()
        self.timer.start()
    
        DriverStation.silenceJoystickConnectionWarning(True)
        self.autonomous = self.autoChooser.getSelected()

        if self.autonomous:
            self.autonomous.schedule()

    def autonomousPeriodic(self) -> None:
        try:
            if self.autoSelected == "disabled":
                return

            if self.autoSelected == "center":
                self.drive.arcadeDrive(0.5, 0)

                timer = self.timer.get()
                if timer < 2:
                    self.drivetrain.arcadeDriveAuto(-0.4,0)
                    self.shooter.activate()
                elif 2 < timer < 10:
                    self.drivetrain.arcadeDriveAuto(0,0)
                    self.indexer.feed(-0.35, -0.8)
                else:
                    self.shooter.deactivate()
                    self.indexer.feed(0,0)
                    self.drivetrain.arcadeDriveAuto(0,0)

            elif self.autoSelected == "left" or self.autoSelected == "right":
                if timer < 2:
                    self.shooter.setFlywheel(0.60)
                elif 2 < timer < 10:
                    self.indexer.activateFeed()
                else:
                    self.shooter.setFlywheel(0)
                    self.indexer.feed(0,0)
        except BaseException as e:
            print(f"Error in autonomousPeriodic: {e}")

    def autonomousExit(self) -> None:
        CommandScheduler.getInstance().cancelAll()
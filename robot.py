from drivetrain import Drivetrain
from photonvisioncamera import PhotonVisionCamera
from genericjoystick import GenericJoystick
from autonomous.basicauto import BasicAuto
from intake import Intake
from shooter import Shooter
from commands2 import TimedCommandRobot, CommandScheduler, Command
from typing import Optional
from commands2.cmd import run
import constants

class Robot(TimedCommandRobot):
    autonomous: Optional[Command] = None

    def robotInit(self) -> None:
        self.camera = PhotonVisionCamera(constants.kCameraName)
        self.drivetrain = Drivetrain(self.camera)
        self.intake = Intake()
        self.shooter = Shooter(0, 0.1, 0, 100)

        self.driver_joystick = GenericJoystick(
            constants.kJoystickDriverPort
        )

        self.drivetrain.setDefaultCommand(
            run(
                lambda: self.drivetrain.arcadeDrive(
                    self.driver_joystick.getLeftYAxis(),
                    self.driver_joystick.getRightXAxis()
                ),
                self.drivetrain
            )
        )

    def autonomousInit(self) -> None:
        self.autonomous = BasicAuto(self.drivetrain)
        self.autonomous.schedule()
    
    def autonomousExit(self) -> None:
        CommandScheduler.getInstance().cancelAll()
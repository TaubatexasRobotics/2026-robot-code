from drivetrain import Drivetrain
from genericjoystick import GenericJoystick
from autonomous.basicauto import BasicAuto
from commands2 import TimedCommandRobot, CommandScheduler, Command
from typing import Optional
from commands2.cmd import run
import constants

class Robot(TimedCommandRobot):
    autonomous: Optional[Command] = None

    def robotInit(self) -> None:
        self.drivetrain = Drivetrain()

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

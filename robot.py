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


class Robot(TimedCommandRobot):
    autonomous: Optional[Command] = None

    def robotInit(self) -> None:
        #self.drivetrain = Drivetrain()
        self.turret = Turret()
        self.intake = Intake()
        self.camera = LimelightCamera("172.29.0.1")
        self.driver_joystick = GenericJoystick(constants.kJoystickDriverPort)

        JoystickButton(self.driver_joystick, 1).onTrue(
            run(
                lambda: self.intake.startPivotUp(),
                self.intake
            )
        )

        JoystickButton(self.driver_joystick, 2).onTrue(
            run(
                lambda: self.intake.startPivotDown(),
                self.intake
            )
        )

        '''self.drivetrain.setDefaultCommand(
            run(
                lambda: self.drivetrain.arcadeDrive(
                    self.driver_joystick.getLeftYAxis(),
                    self.driver_joystick.getRightXAxis(),
                ),
                self.drivetrain,
            )
        )
        '''
    def autonomousInit(self) -> None:
        #self.autonomous = BasicAuto(self.drivetrain)
        #self.autonomous.schedule()
        pass

    def autonomousExit(self) -> None:
        CommandScheduler.getInstance().cancelAll()

    def teleopPeriodic(self) -> None:
        # if self.driver_joystick.getRawButtonPressed(1):
        self.turret.turretAlign(16, self.camera)
        # else:
        #     self.turret.stop()

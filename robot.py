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
from turret import Turret
from camera import Pixy2, LimelightCamera, PhotonVisionCamera
from crest import Crest

class Robot(TimedCommandRobot):
    # autonomous: Optional[Command] = None
    drivetrain: Drivetrain = Drivetrain()
    # intake: Intake = Intake()
    # # autoChooser: SendableChooser = AutoBuilder.buildAutoChooser()
    driverJoystick: GenericJoystick = GenericJoystick(constants.kJoystickDriverPort)
    # shooter: Shooter = Shooter()
    turret: Turret = Turret()
    crest: Crest = Crest()

    def robotInit(self) -> None:
        # definicao dos botoes
        JoystickButton(self.driverJoystick, 1).whileTrue(self.crest.commandMoveToSetpoint())
        JoystickButton(self.driverJoystick, 2).whileTrue(self.drivetrain.forward())
        JoystickButton(self.driverJoystick, 3).whileTrue(self.drivetrain.backward())
        JoystickButton(self.driverJoystick, 4).whileTrue(self.drivetrain.aim(20))#Tag aleatoria da apriltag
        JoystickButton(self.driverJoystick, 5).whileTrue(self.turret.commandCenterTurret(self.driverJoystick.getLeftXAxis()))
        JoystickButton(self.driverJoystick, 6).whileTrue(self.drivetrain.aimAndRange(20))#Tag aleatora
        JoystickButton(self.driverJoystick, 7).whileTrue()
        JoystickButton(self.driverJoystick, 8).whileTrue()
        JoystickButton(self.driverJoystick, 9).whileTrue()

        '''
        self.autoChooser.addOption(
            "LTV Controller Test Auto", AutoLTVController(self.drivetrain)
        )
        self.autoChooser.addOption(
            "Drive Straight Path", DriveStraightPath(self.drivetrain, 5)
        )
        SmartDashboard.putData("Auto Chooser", self.autoChooser)
        '''
    def teleopInit(self) -> None:
        pass
    
    def testPeriodic(self):
        pass
        '''
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
        '''

    def autonomousInit(self) -> None:
        pass
        '''
        DriverStation.silenceJoystickConnectionWarning(True)
        self.autonomous = self.autoChooser.getSelected()

        if self.autonomous:
            self.autonomous.schedule()
        '''

    def autonomousPeriodic(self) -> None:
        pass

    def autonomousExit(self) -> None:
        CommandScheduler.getInstance().cancelAll()

    # def testInit(self) -> None:
    #     JoystickButton(self.driverJoystick, 1).onTrue(
    #         self.shooter.setFlywheelBySetpointCommand()
    #     )

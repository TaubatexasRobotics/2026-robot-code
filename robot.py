from commands2 import TimedCommandRobot, CommandScheduler, Command, ParallelCommandGroup, SequentialCommandGroup
from RampJoystick import RampJoystick
from drivetrain import Drivetrain
import constants
from commands2.button import JoystickButton, POVButton, CommandXboxController
from intake import Intake
from gate import Gate

class MyRobot(TimedCommandRobot):
    def combineAxis(self, joystick: RampJoystick, left_axis, right_axis) -> float:
        leftTrigger = -joystick.getRawAxis(left_axis)
        rightTrigger = joystick.getRawAxis(right_axis)
        return rightTrigger + leftTrigger
    
    def combineRampAxis(self, joystick: RampJoystick, left_axis, right_axis) -> float:
        leftTrigger = -joystick.getRampAxis(left_axis)
        rightTrigger = joystick.getRampAxis(right_axis)
        return rightTrigger + leftTrigger
    
    def robotInit(self) -> None:
        # Joysticks
        self.driver_joystick = RampJoystick(constants.Kdriver_joystick,0.5,0.8,0.8,0.2)
        self.copilot_joystick = CommandXboxController(constants.Kcopilot_joystick)
        self.codriver_joystick = RampJoystick(constants.Kcopilot_joystick,0.5,0.8,0.8,0.2)

        # Subsystens
        self.drivetrain = Drivetrain()
        self.intake = Intake()
        self.gate = Gate()
        
        # Driver joystick buttons
        # Drivetrain        
        self.drivetrain.setDefaultCommand(
            self.drivetrain.arcadeDriveCommand(
                lambda: -self.combineRampAxis(self.driver_joystick, 2, 3),
                lambda: self.driver_joystick.getRampAxis(0)
            )
        )

        # Copilot joystick buttons
        # Intake Pivot 
        self.copilot_joystick.povUp().whileTrue(self.intake.upPivotByCurrent())
        self.copilot_joystick.povUpRight().whileTrue(self.intake.upPivotByCurrent())
        self.copilot_joystick.povUpLeft().whileTrue(self.intake.upPivotByCurrent())
        
        self.copilot_joystick.povDown().whileTrue(self.intake.downPivotByCurrent())
        self.copilot_joystick.povDownRight().whileTrue(self.intake.downPivotByCurrent())
        self.copilot_joystick.povDownLeft().whileTrue(self.intake.downPivotByCurrent())

        # POVButton(self.codriver_joystick, 0).whileTrue(
        #     self.intake.upPivotByCurrent()
        # )
        # POVButton(self.codriver_joystick, 180).whileTrue(
        #     self.intake.down()
        # )

        # Intake Roller
        self.copilot_joystick.rightTrigger().whileTrue(self.intake.colectGamePiece())
        self.copilot_joystick.leftTrigger().whileTrue(self.intake.releaseGamePiece())

        # Gate
        self.copilot_joystick.rightBumper().whileTrue(self.gate.openGate())
        self.copilot_joystick.leftBumper().whileTrue(self.gate.closeGate())

    def autonomousInit(self) -> None:
        pass

    def autonomousPeriodic(self) -> None:
        pass

    def autonomousExit(self) -> None:
        pass

    def teleopInit(self) -> None:
        pass

    def teleopPeriodic(self) -> None:    
        pass
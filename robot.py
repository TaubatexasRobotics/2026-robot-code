from commands2 import TimedCommandRobot, CommandScheduler, Command, ParallelCommandGroup, SequentialCommandGroup
from RampJoystick import RampJoystick
from drivetrain import Drivetrain
import constants
from commands2.button import JoystickButton, POVButton
from intake import Intake

class MyRobot(TimedCommandRobot):

    driverJoystick: RampJoystick = RampJoystick(constants.Kdriver_joystick, 0,0,0,0)
    copilotJoystick : RampJoystick = RampJoystick(constants.Kcodriver_joystick, 0,0,0,0)
    
    def combineAxis(self, joystick: RampJoystick, left_axis, right_axis) -> float:
        leftTrigger = -joystick.getRawAxis(left_axis)
        rightTrigger = joystick.getRawAxis(right_axis)
        return rightTrigger + leftTrigger
    
    def combineRampAxis(self, joystick: RampJoystick, left_axis, right_axis) -> float:
        leftTrigger = -joystick.getRampAxis(left_axis)
        rightTrigger = joystick.getRampAxis(right_axis)
        return rightTrigger + leftTrigger
    
    def robotInit(self) -> None:
        self.driver_joystick : RampJoystick = RampJoystick(constants.Kdriver_joystick,0.5,0.7,0.8,0.2)
        self.codriver_joystick : RampJoystick = RampJoystick(constants.Kcodriver_joystick,0.5,0.7,0.8,0.2)
        self.drivetrain : Drivetrain = Drivetrain()
        self.intake : Intake = Intake() 
        
        # Driver joystick buttons
        JoystickButton(self.driverJoystick, 3).toggleOnTrue(self.intake.colectGamePiece())

        JoystickButton(self.driverJoystick, 4).whileTrue(self.intake.releaseGamePiece())
        
        self.drivetrain.setDefaultCommand(
            self.drivetrain.arcadeDriveCommand(
                lambda: -self.combineAxis(self.driverJoystick, 2, 3),
                lambda: self.driverJoystick.getRawAxis(0)
            )
        )

        # Copilot joystick buttons
        POVButton(self.copilotJoystick, 0).whileTrue(
            self.intake.up()
        )

        POVButton(self.copilotJoystick, 180).whileTrue(
            self.intake.down()
        )
        
    def teleopInit(self) -> None:
        
        self.drivetrain.setDefaultCommand(
            self.drivetrain.arcadeDriveCommand(
                lambda: -self.combineRampAxis(self.driver_joystick, 2, 3),
                lambda: self.driver_joystick.getRawAxis(0)
            ) 
        )

    def teleopPeriodic(self) -> None:    
        pass
        # self.drivetrain.arcadeDrive(self.joystick.getRampAxis(1), self.joystick.getRampAxis(0),False)
        #self.motor1.set(self.joystick.getRampAxis(1))
        #self.motor2.set(self.joystick.getRampAxis(0))
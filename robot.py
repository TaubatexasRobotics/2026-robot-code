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
        self.driver_joystick = RampJoystick(constants.Kdriver_joystick,0.5,0.7,0.8,0.2)
        self.codriver_joystick = RampJoystick(constants.Kcodriver_joystick,0.5,0.7,0.8,0.2)
        self.codriver_xbox_controller = CommandXboxController(constants.Kcodriver_joystick)
        # Subsystens
        self.drivetrain = Drivetrain()
        self.intake = Intake()
        self.gate = Gate()
        
        # Driver joystick buttons
        
        # Drivetrain        
        self.drivetrain.setDefaultCommand(
            self.drivetrain.arcadeDriveCommand(
                lambda: -self.combineAxis(self.driver_joystick, 2, 3),
                lambda: self.driver_joystick.getRawAxis(0)
            )
        )

        # Copilot joystick buttons
        
        # Intake Pivot 
        POVButton(self.codriver_joystick, 0).whileTrue(
            self.intake.up()
        )
        POVButton(self.codriver_joystick, 180).whileTrue(
            self.intake.down()
        )

        # Intake Roller
        self.codriver_xbox_controller.rightTrigger().whileTrue(self.intake.colectGamePiece())
        self.codriver_xbox_controller.leftTrigger().whileTrue(self.intake.releaseGamePiece())

        # Gate
        self.codriver_xbox_controller.rightBumper().whileTrue(self.gate.openGate())
        self.codriver_xbox_controller.leftBumper().whileTrue(self.gate.closeGate())


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
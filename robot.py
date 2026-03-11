from wpilib import Joystick
from commands2 import TimedCommandRobot, Command
from RampJoystick import RampJoystick
from phoenix5 import WPI_VictorSPX
from wpilib.drive import DifferentialDrive
from drivetrain import Drivetrain
import constants

class MyRobot(TimedCommandRobot):
    def combineAxis(self, joystick: RampJoystick, left_axis, right_axis) -> float:
        leftTrigger = -joystick.getRawAxis(left_axis)
        rightTrigger = joystick.getRawAxis(right_axis)
        return rightTrigger + leftTrigger
    
    def robotInit(self) -> None:
        self.driver_joystick = RampJoystick(constants.Kdriver_joystick,0.5,0.7,0.8,0.2)
        self.codriver_joystick = RampJoystick(constants.Kcodriver_joystick,0.5,0.7,0.8,0.2)
        self.drivetrain = Drivetrain()
        
    def teleopInit(self) -> None:
        
        self.drivetrain.setDefaultCommand(
            self.drivetrain.arcadeDriveCommand(
                lambda: -self.combineAxis(self.driver_joystick, 2, 3),
                lambda: self.driver_joystick.getRawAxis(0)
            ) 
        )

    def teleopPeriodic(self) -> None:    
        pass
        # self.drivetrain.arcadeDrive(self.joystick.getRampAxis(1), self.joystick.getRampAxis(0),False)
        #self.motor1.set(self.joystick.getRampAxis(1))
        #self.motor2.set(self.joystick.getRampAxis(0))
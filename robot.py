from wpilib import Joystick
from commands2 import TimedCommandRobot, Command
from RampJoystick import RampJoystick
from phoenix5 import WPI_VictorSPX
from wpilib.drive import DifferentialDrive
from drivetrain import Drivetrain
import constants

class MyRobot(TimedCommandRobot):
    def combineAxis(self, joystick: Joystick, left_axis, right_axis) -> float:
        leftTrigger = -joystick.getRawAxis(left_axis)
        rightTrigger = joystick.getRawAxis(right_axis)
    
    def robotInit(self):
        self.driver_joystick = RampJoystick(constants.Kdriver_joystick,0.5,0.7,0.8,0.2)
        self.codriver_joystick = RampJoystick(constants.Kcodriver_joystick,0.5,0.7,0.8,0.2)
        self.drivetrain = Drivetrain()
        
    def teleopInit(self):
        
        self.drivetrain.setDefaultCommand(
            self.drivetrain.arcadeDriveCommand(
                lambda: -self.combineAxis(self.driver_joystick, 2, 3),
                lambda: self.driverJoystick.getRawAxis(0)
            )
        )

    def teleopPeriodic(self):
        pass
        # self.drivetrain.arcadeDrive(self.joystick.getRampAxis(1), self.joystick.getRampAxis(0),False)
        #self.motor1.set(self.joystick.getRampAxis(1))
        #self.motor2.set(self.joystick.getRampAxis(0))
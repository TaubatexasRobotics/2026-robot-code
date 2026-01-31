from drivetrain import Drivetrain
from camera import AprilTagCamera
from turret import Turret
from genericjoystick import GenericJoystick
from wpilib import TimedRobot
from intake import Intake
import constants

class Robot(wpilib.TimedRobot):
    def robotInit(self) -> None:
        self.camera = AprilTagCamera(constants.kCameraName)
        self.drivetrain = Drivetrain(self.camera)
        self.intake = Intake()

        self.driver_joystick = GenericJoystick(constants.kJoystickDriverPort)
        self.codriver_joystick = GenericJoystick(constants.kJoystickCoDriverPort)

    def robotPeriodic(self) -> None:
        self.drivetrain.updateOdometry()

    def teleopPeriodic(self) -> None:
        '''
        if self.joystick.getRawButton(1):
          self.intake.testeMotor()
        elif self.joystick.getRawButton(2):
          self.intake.Contrario()
        else:
            self.intake.arm_motor.set(0)
        '''

        if self.driver_joystick.getA():
          self.intake.ativar(-0.7)
        elif self.driver_joystick.getB():
          self.intake.ativar(0)
        elif self.driver_joystick.getX():
          self.intake.clockwise()
        elif self.driver_joystick.getY():
          self.intake.counterClockwise()        
        else:
            self.intake.arm_motor.set(0)
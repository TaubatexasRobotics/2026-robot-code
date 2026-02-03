from drivetrain import Drivetrain
from camera import AprilTagCamera
from turret import Turret
from genericjoystick import GenericJoystick
from wpilib import TimedRobot, Joystick
from intake import Intake
import constants

class Robot(TimedRobot):
    def robotInit(self) -> None:
        self.camera = AprilTagCamera(constants.kCameraName)
        self.drivetrain = Drivetrain(self.camera)
        self.intake = Intake()

        #self.driver_joystick = GenericJoystick(constants.kJoystickDriverPort)
        #self.codriver_joystick = GenericJoystick(constants.kJoystickCoDriverPort)
        self.driver_joystick = Joystick(0)

    def robotPeriodic(self) -> None:
        self.drivetrain.updateOdometry()

    def teleopPeriodic(self) -> None:
        if self.driver_joystick.getRawButton(1):
            self.intake.turnUp()
        elif self.driver_joystick.getRawButton(2):
            self.intake.turnDown()
        else:
            self.intake.stopArm()
        
        if self.driver_joystick.getRawButton(3):
            self.intake.suckBalls()
        elif self.driver_joystick.getRawButton(4):
            self.intake.dropBalls()
        else:
            self.intake.stopRoll()
          
        self.drivetrain.arcadeDrive(
          -self.driver_joystick.getRawAxis(1),
          self.driver_joystick.getRawAxis(0)
        )

        '''
        self.isIntakeEnabled = False

          if self.joystick.getRawButtonPressed(1):
        self.isIntakeEnabled = not self.isIntakeEnabled  

        if self.isIntakeEnabled:
            self.intake.suckBalls()
            print("sucking balls")
        else:
            if self.joystick.getRawButton(4):
            self.intake.dropBalls()
            print("drop balls")
            else:
            self.intake.stopRoll()
            print("stop roll")

        if self.joystick.getRawButton(2):
            print("arm down")
            self.intake.turnDown()
        elif self.joystick.getRawButton(3):
            self.intake.turnUp()
            print("arm up")
        else:
            self.intake.stopArm()
            print("arm stopped")
        '''
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
        self.is_intake_enabled = False

    def robotPeriodic(self) -> None:
        self.drivetrain.updateOdometry()

    def teleopPeriodic(self) -> None:
        if self.driver_joystick.getRawButton(1):
            self.intake.turnUp()
        elif self.driver_joystick.getRawButton(2):
            self.intake.turnDown()
        else:
            self.intake.stopArm()
          
        self.drivetrain.arcadeDrive(
          self.driver_joystick.getRawAxis(1),
          self.driver_joystick.getRawAxis(4)
        )

        
        if self.driver_joystick.getRawButtonPressed(1):
            self.is_intake_enabled = not self.is_intake_enabled  

        if self.is_intake_enabled:
            self.intake.suckBalls()
            #print("sucking balls")
        else:
            if self.driver_joystick.getRawButton(4):
                self.intake.dropBalls()
                #print("drop balls")
            else:
                self.intake.stopRoll()
                #print("stop roll")
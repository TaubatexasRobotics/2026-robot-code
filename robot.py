from drivetrain import Drivetrain
from camera import PhotonVisionCamera
from turret import Turret
from genericjoystick import GenericJoystick
from wpilib import TimedRobot, Joystick
from intake import Intake
import constants
from limelight_camera import LimeLightCamera

class Robot(TimedRobot):
    def robotInit(self) -> None:
        self.camera = PhotonVisionCamera(constants.kCameraName)
        self.drivetrain = Drivetrain(self.camera)
        self.intake = Intake()
        self.limelight = LimeLightCamera()

        self.driver_joystick = GenericJoystick(constants.kJoystickDriverPort)
        #self.codriver_joystick = GenericJoystick(constants.kJoystickCoDriverPort)
        self.is_intake_enabled = False

    def robotPeriodic(self) -> None:
        self.drivetrain.updateOdometry()
        self.limelight.logging()

    def teleopPeriodic(self) -> None:
        if self.driver_joystick.getA():
            self.intake.turnUp()
        elif self.driver_joystick.getB():
            self.intake.turnDown()
        else:
            self.intake.stopArm()
          
        self.drivetrain.arcadeDrive(
          self.driver_joystick.getLeftYAxis(),
          self.driver_joystick.getRightXAxis()
        )
        
        if self.driver_joystick.getX():
            self.is_intake_enabled = not self.is_intake_enabled  

        if self.is_intake_enabled:
            self.intake.suckBalls()
            #print("sucking balls")
        else:
            if self.driver_joystick.getY():
                self.intake.dropBalls()
                #print("drop balls")
            else:
                self.intake.stopRoll()
                #print("stop roll")

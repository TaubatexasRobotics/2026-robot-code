from drivetrain import Drivetrain
from photonvisioncamera import PhotonVisionCamera
from turret import Turret
from genericjoystick import GenericJoystick
from wpilib import TimedRobot, SmartDashboard
from intake import Intake
import constants
from shooter import Shooter

class Robot(TimedRobot):
    def robotInit(self) -> None:
        self.camera = PhotonVisionCamera(constants.kCameraName)
        self.drivetrain = Drivetrain(self.camera)
        self.intake = Intake()
        self.shooter = Shooter(0, 0.1, 0, 100)

        self.driver_joystick = GenericJoystick(constants.kJoystickDriverPort)

        SmartDashboard.putNumber("kS", 0.1)

    def robotPeriodic(self) -> None:
        self.drivetrain.periodic()
        self.shooter.setFeedforwardConstraints(
            SmartDashboard.getNumber("kS", 0),
            0,
            0
        )

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
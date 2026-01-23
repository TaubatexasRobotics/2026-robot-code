import wpilib
from wpilib import TimedRobot
from drivetrain import Drivetrain
from camera import AprilTagCamera
from turret import Turret

class Robot(wpilib.TimedRobot):
    def robotInit(self) -> None:
        self.camera = AprilTagCamera("Camera7459")
        self.drivetrain = Drivetrain(self.camera)
        self.turret = Turret(self.camera)
        self.joystick = wpilib.Joystick(0)


    def teleopPeriodic(self) -> None:
        #self.drivetrain.arcadeDriveAimAndRange(3)
        
        if self.joystick.getRawButton(1):
            self.turret.yawLeft()
        elif self.joystick.getRawButton(3):
            self.turret.yawRight()
        elif self.joystick.getRawButton(2):
            self.turret.TurretAlign(1)
        else:
            self.turret.turnOffKraken()
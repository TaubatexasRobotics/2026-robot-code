import wpilib
from Turret import Turret
class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.turret = Turret()
        self.joystick = wpilib.Joystick(0)

    def robotPeriodic(self):
        self.turret.update()

    def teleopPeriodic(self):
        if self.joystick.getRawButton(1):
            self.turret.shoot()
        else:
            self.turret.stop() 
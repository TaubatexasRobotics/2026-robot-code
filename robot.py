import wpilib
import Turret

class MyRobot (wpilib.TimedRobot):

    def robotInit(self):
        self.torreta = Turret.Turret()
        self.joystick = wpilib.Joystick(0)

    def teleopPeriodic(self):

        if self.joystick.getRawButton(1):
            self.torreta.turnLeft()
        elif self.joystick.getRawButton(2):
            self.torreta.turnRight()    
        else:
            self.torreta.stopTurret()    



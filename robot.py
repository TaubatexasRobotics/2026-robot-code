import wpilib
from shooter import Shooter

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.hood = Shooter()
        self.joystick = wpilib.Joystick(0)
        self.dashboard = wpilib.SmartDashboard
        wpilib.SmartDashboard.putNumber("setpoint", 0)


    def teleopPeriodic(self):
        self.hood.update_dashboard()

        if self.joystick.getRawButton(1):
            self.hood.up()
        elif self.joystick.getRawButton(2):
            self.hood.down()
        else:
            self.hood.stop()    


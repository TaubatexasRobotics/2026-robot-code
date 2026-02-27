import wpilib
from crest import Crest

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.crest = Crest()
        self.joystick = wpilib.Joystick(0)
        self.dashboard = wpilib.SmartDashboard
        wpilib.SmartDashboard.putNumber("setpoint", 0)


    def teleopPeriodic(self):
        self.crest.update_dashboard()

        self.crest.move_to_setpoint()


        # if self.joystick.getRawButton(1):
        #   self.crest.up()
        # elif self.joystick.getRawButton(2):
        #   self.crest.down()
        # else:
        #     self.crest.stop()
        
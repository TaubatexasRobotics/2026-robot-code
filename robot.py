import wpilib
from intake import Intake
from indexer import Indexer
from hood import Hood
from shooter import Shooter
from turret import Turret
from drivetrain import Drivetrain
from commands2 import TimedCommandRobot
from utils import for_each

def log_exception(e):
    wpilib.DataLogManager.log(repr(e))
    
class MyRobot(TimedCommandRobot):
    def robotInit(self):
        self.mechanisms = {
            "intake": Intake(),
            "crest": Hood(),
            "drivetrain": Drivetrain(),
            "shooter": Shooter(),
            "indexer": Indexer(),
            "turret": Turret()
        }
        
    def robotPeriodic(self):
        for_each(self.mechanisms, "update_dashboard")

    def teleopPeriodic(self):
        for_each(self.mechanisms, "teleopPeriodic")
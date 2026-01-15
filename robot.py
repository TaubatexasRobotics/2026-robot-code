import wpilib
import rev
import wpilib.drive
class Robot(wpilib.TimedRobot):
    def RobotInit(self):
        self.shooter1 = rev.SparkMax(1, rev.SparkLowLevel.MotorType.kBrushless)
        self.joystick = wpilib.Joystick(0)
    def teleopPeriodic(self):
        if self.joystick.getRawButtonPressed(0):
            self.shooter1.set(1)
    

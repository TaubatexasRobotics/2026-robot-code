import wpilib
import rev
import phoenix6
import phoenix5

class Climber:
    def __init__(self):
        self.left_motor = phoenix5.WPI_VictorSPX(1)
        self.right_motor = phoenix5.WPI_VictorSPX(2)
        self.climber = wpilib.MotorControllerGroup(self.left_motor, self.right_motor)

    def climb(self, speed):
        self.climber.set(1)

    def stop(self):
        self.climber.set(0)

    def down(self):
        self.climber.set(-1)
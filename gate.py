from phoenix5 import WPI_VictorSPX
from commands2 import Subsystem, Command
import constants

OPEN_SPEED = 0.6
CLOSE_SPEED = -0.3

class Gate(Subsystem):

    def __init__(self):
        self.motor_gate = WPI_VictorSPX(constants.Kgate_motor_id)

        self.setDefaultCommand(self.stopGate())

    def openGate(self) -> Command:
        return self.run(lambda: self.motor_gate.set(OPEN_SPEED))      

    def closeGate(self) -> Command:
        return self.run(lambda: self.motor_gate.set(CLOSE_SPEED))      

    def stopGate(self) -> Command:
        return self.run(self.motor_gate.stopMotor)
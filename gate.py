from phoenix5 import WPI_VictorSPX
from commands2 import Subsystem, Command
import constants

class Gate(Subsystem):

    def __init__(self):
        self.motor_gate = WPI_VictorSPX(constants.Kgate_motor_id)

    def openGate(self):
        return self.run(lambda: self.motor_gate.set(0.5))      

    def closeGate(self):
        return self.run(lambda: self.motor_gate.set(-0.5))      

    def stopGate(self) -> Command:
        return self.run(self.motor_gate.stopMotor)

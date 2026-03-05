from wpilib import SerialPort, Solenoid, PneumaticsModuleType
from commands2 import Command, Subsystem
import constants

class LEDController(Subsystem):
    def __init__(self) -> None:
        self.arduino = SerialPort(constants.kBaudRate, constants.kLEDUSBPort)
        self.extraLED = Solenoid(PneumaticsModuleType.CTREPCM, 4)
        self.status = "off"

    def red(self) -> Command:
        return self.run(lambda: self.changeColor("r"))

    def green(self) -> Command:
        return self.run(lambda: self.changeColor("g"))

    def blue(self) -> Command:
        return self.run(lambda: self.changeColor("b"))

    def blinkGreen(self) -> Command:
        return self.run(lambda: self.changeColor("w"))

    def rainbow(self) -> Command:
        return self.run(lambda: self.changeColor("a"))

    def setExtraLED(self, status: bool) -> None:
        return self.extraLED.set(status)

    def changeColor(self, char: str) -> None:
        if self.status == char:
            return
        self.status = char
        byte_obj = char.encode("ascii")
        self.arduino.write(byte_obj)

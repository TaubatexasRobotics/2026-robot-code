from wpilib import SerialPort, Solenoid, PneumaticsModuleType
import constants

class LEDController:
    def __init__(self) -> None:
        self.arduino = SerialPort(constants.kBaudRate, constants.kLEDUSBPort)
        self.extraLED = Solenoid(PneumaticsModuleType.CTREPCM, 4)

    def red(self) -> None:
        self.changeColor("r")

    def green(self) -> None:
        self.changeColor("g")

    def blue(self) -> None:
        self.changeColor("b")

    def setExtraLED(self, status: bool) -> None:
        self.extraLED.set(status)

    def changeColor(self, char: str) -> None:
        byte_obj = char.encode("ascii")
        self.arduino.write(byte_obj)

from wpilib import SerialPort
from dataclasses import dataclass
import constants

@dataclass
class LEDController:
    arduino: SerialPort = SerialPort(constants.kBaudRate, constants.kLEDUSBPort)

    def red(self) -> None:
        self.changeColor("r")

    def green(self) -> None:
        self.changeColor("g")

    def blue(self) -> None:
        self.changeColor("b")

    def changeColor(char: str) -> None:
        byte_obj = char.encode("ascii")
        self.arduino.write(byte_obj)

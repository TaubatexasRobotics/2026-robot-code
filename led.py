from wpilib import SerialPort
import constants

class LEDController:
    def __init__(self) -> None:
        self.arduino = SerialPort(constants.kBaudRate, constants.kLEDUSBPort)

from wpilib import SerialPort
import constants

class LEDController:
    def __init__(self) -> None:
        self.arduino = SerialPort(
            constants.kBaudRate, 
            constants.kLEDUSBPort
        )

    def activateRedColor(self) -> None:
        changeColor('r')

    def activateGreenColor(self) -> None:
        changeColor('g')

    def activateBlueColor(self) -> None:
        changeColor('b')

    def changeColor(char: str) -> None:
        byte_obj = char.encode('ascii')
        self.arduino.write(byte_obj)


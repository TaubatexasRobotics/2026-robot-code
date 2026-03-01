from math import tan
from wpilib import SerialPort


class Utils:
    @staticmethod
    def calculateDistanceToTargetMeters(
        cameraHeightMeters: float,
        targetHeightMeters: float,
        cameraPitchRadians: float,
        targetPitchRadians: float,
    ) -> float:
        return (targetHeightMeters - cameraHeightMeters) / tan(
            cameraPitchRadians + targetPitchRadians
        )

    @staticmethod
    def readString(port: SerialPort) -> str:
        port_bytes = port.getBytesReceived()
        buffer = bytearray(port_bytes)
        converted = port.read()
        return buffer[:converted].decode("ascii")

    @staticmethod
    def clamp(value, min_value, max_value):
        return max(min(value, max_value), min_value)


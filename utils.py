from math import tan

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
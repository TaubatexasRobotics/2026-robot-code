from photonlibpy import PhotonCamera
import wpimath.units
import constants
from typing import Optional, Tuple
from utils import Utils

from photonlibpy.targeting.photonTrackedTarget import PhotonTrackedTarget

class AprilTagCamera(PhotonCamera):
    def __init__(self, camera: str) -> None:
        self.camera = PhotonCamera(camera)

    def getBestTarget(self) -> Optional[PhotonTrackedTarget]:
        result = self.camera.getLatestResult()
        if result.hasTargets():
            target = result.getBestTarget()
            return target
        return None

    def getYaw(self, tag: int) -> float:
        results = self.camera.getAllUnreadResults()
        if len(results) > 0:
            result = results[-1]
            for target in result.getTargets():
                if target.getFiducialId() == tag:
                    return target.getYaw()
        return -1

    def getYawWithRange(self, tag: int) -> Tuple[float, float]:
        results = self.camera.getAllUnreadResults()
        target_range = 0
        if len(results) > 0:
            result = results[-1]
            for target in result.getTargets():
                if target.getFiducialId() == tag:
                    target_range = Utils.calculateDistanceToTargetMeters(
                        constants.kCameraHeightMeters,
                        constants.kTargetHeightMeters,
                        constants.kCameraPitchRadians,
                        wpimath.units.degreesToRadians(target.getPitch())
                    )
                    return target.getYaw(), target_range
        return -1, -1
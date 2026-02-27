import constants
from photonlibpy import PhotonCamera
from typing import Optional, Tuple, List
from utils import Utils
from abc import ABC, abstractmethod
from limelight import Limelight
from limelightresults import parse_results
from wpinet import PortForwarder
from photonlibpy.targeting.photonTrackedTarget import PhotonTrackedTarget
from wpimath.units import degreesToRadians
from pixy2py.pixy2 import Pixy2
from pixy2py.pixy2ccc import Pixy2CCC
from wpilib import RobotBase, SerialPort, CameraServer


class AprilTagCamera(ABC):
    @abstractmethod
    def getYawFromTag(self, tag: int) -> float:
        pass

    @abstractmethod
    def getYawAndRangeFromTag(self, tag: int) -> Tuple[float, float]:
        pass

class PhotonVisionCamera(AprilTagCamera):
    def __init__(self, camera: str) -> None:
        self.camera = PhotonCamera(camera)

    def getBestTarget(self) -> Optional[PhotonTrackedTarget]:
        result = self.camera.getLatestResult()
        if result.hasTargets():
            target = result.getBestTarget()
            return target
        return None

    def getYawFromTag(self, tag: int) -> float:
        results = self.camera.getAllUnreadResults()
        if len(results) > 0:
            result = results[-1]
            for target in result.getTargets():
                if target.getFiducialId() == tag:
                    return target.getYaw()
        return -1

    def getYawAndRangeFromTag(self, tag: int) -> Tuple[float, float]:
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
                        degreesToRadians(target.getPitch()),
                    )
                    return target.getYaw(), target_range
        return -1, -1


class LimelightCamera(AprilTagCamera):
    def __init__(self, camera: str) -> None:
        self.limelight = None

        if not RobotBase.isSimulation():
            self.limelight = Limelight(camera)
            self.limelight.pipeline_switch(0)

        PortForwarder.getInstance().add(*constants.kLimelightPortForwarder)

    def getYawFromTag(self, tag: int) -> float:
        if self.limelight is None:
            return -1

        result = self.limelight.get_results()
        parsed_result = parse_results(result)

        if parsed_result is None:
            return -1

        for target in parsed_result.fiducialResults:
            if target.fiducial_id == tag:
                return target.target_x_degrees  # yaw

        return -1

    def getYawAndRangeFromTag(self, tag: int) -> Tuple[float, float]:
        return 0, 0

class PixyFuelDetector:
    def __init__(self) -> None:
        self.pixy = Pixy2(Pixy2.LinkType.SPI)
        self.pixy.init()
        self.pixy.setLamp(1, 1)
        self.pixy.setLED(255, 255, 255)

    def getBiggestBlock(self) -> Optional[Pixy2CCC.Block]:
        blockCount: int = pixy.getCCC().getBlocks(False, Pixy2CCC.CCC_SIG1, 25)
        print("Found " + str(blockCount) + " blocks!")
        if blockCount <= 0:
            return None

        blocks = self.pixy.getCCC().getBlockCache()
        largestBlock: Optional[PixyCCC.Block] = None

        for block in blocks:
            if largestBlock is None:
                largestBlock = block
            elif block.getWidth() > largestBlock.getWidth():
                largestBlock = block

        return largestBlock

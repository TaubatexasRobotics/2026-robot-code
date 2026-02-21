import constants
from photonlibpy import PhotonCamera
from typing import Optional, Tuple, List
from dataclasses import dataclass
from utils import Utils
from abc import ABC, abstractmethod
from limelight import Limelight
from limelightresults import parse_results
from wpinet import PortForwarder
from photonlibpy.targeting.photonTrackedTarget import PhotonTrackedTarget
from wpimath.units import degreesToRadians
from wpilib import RobotBase, SerialPort, CameraServer


class AprilTagCamera(ABC):
    @abstractmethod
    def getYawFromTag(self, tag: int) -> float:
        pass

    @abstractmethod
    def getYawAndRangeFromTag(self, tag: int) -> Tuple[float, float]:
        pass

class PixyObject(GenericObject):
    sig: int
    x: int
    y: int
    width: int
    height: int
    index: int
    age: int

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

@dataclass
class Pixy2:
    arduino: SerialPort = SerialPort(constants.kBaudRate, constants.kLEDUSBPort)

    def getCloserGamePiece(self) -> Optional[PixyObject]:
        all_object_transform_data: str = Utils.readString(self.arduino)

        if len(object_transform_data) <= 0:
            return
        
        object_transform_data: List[str] = all_object_transform_data.splitlines()

        final_data: List[str] = object_transform_data[-1].split(":")

        # sig: X x: X y: X width: X height: X index: X age: X
        return PixyObject(
            sig=int(final_data[1]),
            x=int(final_data[3]),
            y=int(final_data[5]),
            width=int(final_data[7]),
            height=int(final_data[9]),
            index=int(final_data[11]),
            age=int(final_data[13])
        )

class DriverCamera:
    def __init__(self) -> None:
        CameraServer().launch()
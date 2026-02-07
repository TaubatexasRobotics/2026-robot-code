from limelight import Limelight
from limelightresults import parse_results

class LimelightCamera:
    def __init__(self, address: str) -> None:
        self.limelight = Limelight(address)

    def getResults(self):
        result = self.limelight.get_latest_results()
        parsed_result = limelightresults.parse_results(result)
        if parsed_result is not None:
            print("valid targets: ", parsed_result.validity, ", pipelineIndex: ", parsed_result.pipeline_id,", Targeting Latency: ", parsed_result.targeting_latency)
                    
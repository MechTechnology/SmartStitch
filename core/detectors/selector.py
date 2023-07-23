from core.utils.constants import DETECTION_TYPE
from ..services import logFunc
from .direct_slicing import DirectSlicingDetector
from .pixel_comparison import PixelComparisonDetector

# Define a function called select_detector, decorated with the logFunc decorator
@logFunc()
def select_detector(detection_type: str | DETECTION_TYPE):
    # Check if the detection_type is set to "none" or "NO_DETECTION" (a constant from DETECTION_TYPE enum)
    if detection_type == "none" or detection_type == DETECTION_TYPE.NO_DETECTION.value:
        # If it is, return an instance of the DirectSlicingDetector class
        return DirectSlicingDetector()
    
    # Check if the detection_type is set to "pixel" or "PIXEL_COMPARISON" (a constant from DETECTION_TYPE enum)
    elif (
        detection_type == "pixel"
        or detection_type == DETECTION_TYPE.PIXEL_COMPARISON.value
    ):
        # If it is, return an instance of the PixelComparisonDetector class
        return PixelComparisonDetector()
    
    # If the detection_type doesn't match any of the expected values, raise an exception
    else:
        raise Exception("Invalid Detection Type")
from core.utils.constants import DETECTION_TYPE

from ..services import logFunc
from .direct_slicing import DirectSlicingDetector
from .pixel_comparison import PixelComparisonDetector


@logFunc()
def select_detector(detection_type: str | DETECTION_TYPE):
    if detection_type == "none" or detection_type == DETECTION_TYPE.NO_DETECTION.value:
        return DirectSlicingDetector()
    elif (
        detection_type == "pixel"
        or detection_type == DETECTION_TYPE.PIXEL_COMPARISON.value
    ):
        return PixelComparisonDetector()
    else:
        raise Exception("Invalid Detection Type")

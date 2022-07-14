from ..services import logFunc
from .direct_slicing import DirectSlicingDetector
from .pixel_comparsion import PixelComparsionDetector


@logFunc()
def select_detector(detection_type: str):
    if detection_type == 'none':
        return DirectSlicingDetector()
    elif detection_type == 'pixel':
        return PixelComparsionDetector()
    else:
        raise Exception("Invalid Detection Type")

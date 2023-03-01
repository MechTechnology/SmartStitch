from ..utils.constants import DETECTION_TYPE, WIDTH_ENFORCEMENT


class AppSettings:
    """Model for holding Application Settings"""

    def __init__(self, json_dict: dict[str, any] = None):
        # Core Settings
        self.split_height: int = 5000
        self.output_type: str = '.png'
        self.lossy_quality: str = 100
        self.detector_type: DETECTION_TYPE = DETECTION_TYPE.PIXEL_COMPARISON
        self.senstivity: int = 90
        self.ignorable_pixels: int = 5
        self.scan_step: int = 5
        self.enforce_type: WIDTH_ENFORCEMENT = WIDTH_ENFORCEMENT.NONE
        self.enforce_width: int = 720
        self.run_postprocess: bool = False
        self.postprocess_app: str = ""
        self.postprocess_args: str = ""
        self.last_browse_location: str = ""

        if json_dict is not None:
            for key, value in json_dict.items():
                setattr(self, key, value)

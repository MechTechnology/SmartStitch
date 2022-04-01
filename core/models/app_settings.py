from core.utils.constants import WIDTH_ENFORCEMENT


class AppSettings:
    """Model for holding Application Settings"""

    def __init__(self, dict: dict[str, any] = None):
        # Core Settings
        self.split_height: int = 5000
        self.output_type: str = '.png'
        self.senstivity: int = 90
        self.ignorable_pixels: int = 0
        self.scan_step: int = 5
        self.enforce_type: WIDTH_ENFORCEMENT = WIDTH_ENFORCEMENT.NONE
        self.enforce_width: int = 720
        self.subprocess_app: str = ""
        self.subprocess_arguments: str = ""

        if dict is not None:
            for key, value in dict.items():
                setattr(self, key, value)

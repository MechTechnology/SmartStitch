from ..utils.constants import DETECTION_TYPE, WIDTH_ENFORCEMENT

# Define the class AppSettings
class AppSettings:
    """Model for holding Application Settings"""

    # Constructor to initialize the settings with default values
    def __init__(self, json_dict: dict[str, any] = None):
        # Core Settings
        self.split_height: int = 5000                                         # The height at which images are split during processing
        self.output_type: str = '.png'                                        # The type of output image format (e.g., PNG)
        self.lossy_quality: str = 100                                         # The quality of lossy compression (if applicable)
        self.detector_type: DETECTION_TYPE = DETECTION_TYPE.PIXEL_COMPARISON  # The type of detector used
        self.senstivity: int = 90                                             # The sensitivity level of the detector
        self.ignorable_pixels: int = 5                                        # Number of ignorable pixels for the detector
        self.scan_step: int = 5                                               # The step size for scanning during detection
        self.enforce_type: WIDTH_ENFORCEMENT = WIDTH_ENFORCEMENT.NONE         # The type of width enforcement
        self.enforce_width: int = 720                                         # The enforced width (if applicable)
        self.run_postprocess: bool = False                                    # Flag to determine if post-processing is enabled
        self.postprocess_app: str = ""                                        # The post-processing application to run
        self.postprocess_args: str = ""                                       # Arguments for the post-processing application
        self.last_browse_location: str = ""                                   # The last location browsed for input files
        self.last_waifu2x_location: str = ""                                  # The last location selected Waifu2X-Caffe
        self.waifu2x: bool = False                                            # Flag if Waifu2x-Caffe is enabled
        self.waifu2x_noise: bool = False                                      # Flag if Waifu2x-Caffe remove noise is enabled
        self.waifu2x_enlarge: bool = False                                    # Flag if Waifu2x-Caffe enlarge photo is enabled
        self.waifu2x_noise_level: int = 0                                     # The last remove noise level set
        self.waifu2x_enlarge_level: float = 1.60                              # The last enlarge photo level set

        # If a JSON dictionary is provided, update the settings based on its contents
        if json_dict is not None:
            for key, value in json_dict.items():
                setattr(self, key, value)       # Set the attribute with the corresponding value from the dictionary
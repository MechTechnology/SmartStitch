from enum import IntEnum

# Define static variables
LOG_REL_DIR = '__logs__'  # Relative directory for log files
SETTINGS_REL_DIR = '__settings__'  # Relative directory for settings files
OUTPUT_SUFFIX = ' [stitched]'  # Suffix appended to the output filename
POSTPROCESS_SUFFIX = ' [processed]'  # Suffix appended to the post-processed filename
SUPPORTED_IMG_TYPES = (  # Tuple of supported image file types
    '.png',
    '.webp',
    '.jpg',
    '.jpeg',
    '.jfif',
    '.bmp',
    '.tiff',
    '.tga',
    '.psd',
    '.psb',
)

PHOTOSHOP_FILE_TYPES = (  # Tuple of supported Photoshop file types
    ".psd",
    ".psb"
)

# Define static Enums using IntEnum
class WIDTH_ENFORCEMENT(IntEnum):
    NONE = 0  # No enforcement of width
    AUTOMATIC = 1  # Automatic width enforcement
    MANUAL = 2  # Manual width enforcement

class DETECTION_TYPE(IntEnum):
    NO_DETECTION = 0  # No detection for image stitching
    PIXEL_COMPARISON = 1  # Detection using pixel comparison
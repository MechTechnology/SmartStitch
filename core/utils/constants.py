from enum import IntEnum

# Static Variables
LOG_REL_DIR = '__logs__'
SETTINGS_REL_DIR = '__settings__'
OUTPUT_SUFFIX = ' [stitched]'
POSTPROCESS_SUFFIX = ' [processed]'
SUPPORTED_IMG_TYPES = (
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

PHOTOSHOP_FILE_TYPES = (
    ".psd",
    ".psb"
)

# Static Enums
class WIDTH_ENFORCEMENT(IntEnum):
    NONE = 0
    AUTOMATIC = 1
    MANUAL = 2


class DETECTION_TYPE(IntEnum):
    NO_DETECTION = 0
    PIXEL_COMPARISON = 1

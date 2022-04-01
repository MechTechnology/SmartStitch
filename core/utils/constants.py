from enum import IntEnum

# Static Variables
LOG_REL_DIR = '__logs__'
SETTINGS_REL_DIR = '__settings__'
OUTPUT_SUFFIX = ' [stitched]'
SUBPROCESS_SUFFIX = ' [processed]'
SUPPORTTED_IMG_TYPES = (
    '.png',
    '.webp',
    '.jpg',
    '.jpeg',
    '.jfif',
    '.bmp',
    '.tiff',
    '.tga',
)

# Static Enums


class WIDTH_ENFORCEMENT(IntEnum):
    NONE = 0
    AUTOMATIC = 1
    MANUAL = 2


class DETECTION_TYPE(IntEnum):
    NO_DETECTION = 0
    PIXEL_COMPARSION = 1

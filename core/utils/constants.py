from enum import Enum

# Static Variables
LOG_REL_DIR = 'logs'
OUTPUT_SUFFIX = ' [stitched]'
SUBPROCESS_SUFFIX = ' [processed]'
SUPPORTTED_IMG_TYPES = ('.png', '.webp', '.jpg', '.jpeg', '.jfif', '.bmp', '.tiff', '.tga')

# Static Enums
class WIDTH_ENFORCEMENT(Enum):
  NONE = 0
  AUTOMATIC = 1
  MANUAL = 2

class DETECTION_TYPE(Enum):
  NO_DETECTION = 0
  PIXEL_COMPARSION = 1
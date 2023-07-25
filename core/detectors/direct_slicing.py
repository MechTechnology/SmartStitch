from PIL import Image as pil
from core.services.global_logger import logFunc

# Defining a class called DirectSlicingDetector
class DirectSlicingDetector:
    # Decorating the 'run' method with the 'logFunc' decorator
    @logFunc(inclass=True)
    def run(self, combined_img: pil.Image, split_height: int, **kwargs) -> list[int]:
        # Changes from a pil image to a numpy pixel array
        # Getting the height of the combined_img
        last_row = combined_img.size[1]

        # Initializing some variables
        slice_locations = [0]  # Stores the row positions where the image will be sliced
        row = split_height  # Starting from the given 'split_height'

        # Loop to determine the rows where the image will be sliced
        while row < last_row:
            slice_locations.append(row)
            row += split_height

        # Ensuring the last slice covers the remaining rows if the height is not a multiple of 'split_height'
        if slice_locations[-1] != last_row - 1:
            slice_locations.append(last_row - 1)

        # Returning the list of row positions where the image will be sliced
        return slice_locations
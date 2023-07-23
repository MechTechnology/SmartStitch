import numpy as np
from PIL import Image as pil

from core.services.global_logger import logFunc


class PixelComparisonDetector:
    @logFunc(inclass=True)
    def run(self, combined_img: pil.Image, split_height: int, **kwargs) -> list[int]:
        """Uses Neighbouring pixels comparison to detect ideal slice locations"""
        # Changes from a pil Image to an numpy pixel array
        combined_img = np.array(combined_img.convert('L'))

        # Setting up rest of Detector Parameters
        scan_step = kwargs.get('scan_step', 5)                 # Step size for moving up/down while scanning rows
        ignorable_pixels = kwargs.get('ignorable_pixels', 0)   # Number of pixels to ignore at the edges of each row
        sensitivity = kwargs.get('sensitivity', 90)           # Sensitivity threshold for pixel value differences
        threshold = int(255 * (1 - (sensitivity / 100)))      # Threshold for detecting significant pixel value differences
        last_row = len(combined_img)                          # Index of the last row in the image

        # Initializes some variables
        slice_locations = [0]   # List to store the detected slice locations
        row = split_height      # Starting row for scanning the image
        move_up = True          # Flag indicating whether to move up or down while scanning

        # Detector Main Logic
        while row < last_row:
            row_pixels = combined_img[row]  # Extract the pixel values of the current row
            can_slice = True                # Flag to determine if a slice can be made at the current row

            # Check pixel value differences in the current row to decide if a slice can be made
            for index in range(ignorable_pixels + 1, len(row_pixels) - ignorable_pixels):
                prev_pixel = int(row_pixels[index - 1])
                next_pixel = int(row_pixels[index])
                value_diff = next_pixel - prev_pixel
                if value_diff > threshold or value_diff < -threshold:
                    can_slice = False
                    break

            if can_slice:
                slice_locations.append(row)     # If a slice can be made, add the current row as a slice location
                row += split_height             # Move to the next potential slice location
                move_up = True                  # Reset the move_up flag for the next iteration
                continue

            # If a slice cannot be made at the current row, try moving to the next potential location
            # but avoid slicing too close to the previous slice location (ensuring minimum distance is 40% of split_height)
            if row - slice_locations[-1] <= 0.4 * split_height:
                row = slice_locations[-1] + split_height
                move_up = False
            if move_up:
                row -= scan_step     # Move up in the image and continue scanning
                continue
            row += scan_step         # Move down in the image and continue scanning

        # If the last row was not included as a slice location, add it to the list of slice locations
        if slice_locations[-1] != last_row - 1:
            slice_locations.append(last_row - 1)

        return slice_locations  # Return the list of detected slice locations
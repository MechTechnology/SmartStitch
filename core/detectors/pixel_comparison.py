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
        scan_step = kwargs.get('scan_step', 5)
        ignorable_pixels = kwargs.get('ignorable_pixels', 0)
        sensitivity = kwargs.get('sensitivity', 90)
        threshold = int(255 * (1 - (sensitivity / 100)))
        last_row = len(combined_img)
        # Initializes some variables
        slice_locations = [0]
        row = split_height
        move_up = True
        # Detector Main Logic
        while row < last_row:
            row_pixels = combined_img[row]
            can_slice = True
            for index in range(
                ignorable_pixels + 1, len(row_pixels) - ignorable_pixels
            ):
                prev_pixel = int(row_pixels[index - 1])
                next_pixel = int(row_pixels[index])
                value_diff = next_pixel - prev_pixel
                if value_diff > threshold or value_diff < -threshold:
                    can_slice = False
                    break
            if can_slice:
                slice_locations.append(row)
                row += split_height
                move_up = True
                continue
            if row - slice_locations[-1] <= 0.4 * split_height:
                row = slice_locations[-1] + split_height
                move_up = False
            if move_up:
                row -= scan_step
                continue
            row += scan_step
        if slice_locations[-1] != last_row - 1:
            slice_locations.append(last_row - 1)
        return slice_locations

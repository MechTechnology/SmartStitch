import os
import threading

from PIL import Image as pil
from psd_tools import PSDImage

from ..models import WorkDirectory
from ..utils.constants import PHOTOSHOP_FILE_TYPES, WIDTH_ENFORCEMENT
from ..utils.errors import CancelledError
from .global_logger import logFunc


class ChunkedProcessor:
    """Processes images in bounded chunks to minimize memory usage.

    Instead of loading all images into RAM at once, this processor:
    1. Loads images one at a time into a buffer
    2. When buffer height >= split_height * 1.5, runs detection
    3. Slices and saves complete panels
    4. Keeps remaining bottom portion as new buffer
    5. Repeats until all images are processed

    This keeps peak memory bounded regardless of input size.
    """

    # Buffer triggers processing when it reaches this multiple of split_height
    BUFFER_THRESHOLD_MULTIPLIER = 1.5

    def __init__(
        self,
        img_handler,
        img_manipulator,
        detector,
        cancel_event: threading.Event | None = None,
        progress_callback=None,
    ):
        self.img_handler = img_handler
        self.img_manipulator = img_manipulator
        self.detector = detector
        self.cancel_event = cancel_event or threading.Event()
        self.progress_callback = progress_callback or (lambda *args: None)

    def run(
        self,
        workdirectory: WorkDirectory,
        split_height: int,
        output_type: str = ".png",
        lossy_quality: int = 100,
        enforce_type: WIDTH_ENFORCEMENT = WIDTH_ENFORCEMENT.NONE,
        enforce_width: int = 720,
        sensitivity: int = 90,
        ignorable_pixels: int = 0,
        scan_step: int = 5,
    ) -> WorkDirectory:
        """Runs the chunked processing pipeline for a working directory."""
        # Resolve target width based on enforcement mode
        target_width = self._resolve_target_width(
            workdirectory.input_path, workdirectory.input_files, enforce_type, enforce_width
        )

        buffer_img = None
        img_iteration = 1
        chunk_count = 0
        total_images = len(workdirectory.input_files)

        # Load and process images one at a time
        for i, img_file in enumerate(workdirectory.input_files):
            self._check_cancelled()

            # Load and resize single image
            img_path = os.path.join(workdirectory.input_path, img_file)
            img = self._load_single_image(img_path)
            img = self._resize_single_image(img, enforce_type, target_width)

            # Append to buffer (create or extend)
            if buffer_img is None:
                buffer_img = img
            else:
                buffer_img = self._append_to_buffer(buffer_img, img)

            self._report_progress(
                "Loading", i + 1, total_images, f"Loaded {img_file}"
            )

            # Check if buffer is large enough to process, or if this is the last image
            threshold = int(split_height * self.BUFFER_THRESHOLD_MULTIPLIER)
            should_process = buffer_img.size[1] >= threshold or i == total_images - 1

            if should_process:
                chunk_count += 1

                # Run detector on buffer to find slice points
                slice_points = self.detector.run(
                    buffer_img,
                    split_height,
                    sensitivity=sensitivity,
                    ignorable_pixels=ignorable_pixels,
                    scan_step=scan_step,
                )

                # Slice and save each panel
                for j in range(1, len(slice_points)):
                    self._check_cancelled()
                    upper = slice_points[j - 1]
                    lower = slice_points[j]
                    panel = buffer_img.crop((0, upper, buffer_img.size[0], lower))
                    self.img_handler.save(
                        workdirectory, panel, img_iteration, output_type, lossy_quality
                    )
                    img_iteration += 1

                # Keep remaining bottom portion as new buffer
                last_slice = slice_points[-1]
                if last_slice < buffer_img.size[1]:
                    remainder = buffer_img.crop(
                        (0, last_slice, buffer_img.size[0], buffer_img.size[1])
                    )
                    buffer_img = remainder
                else:
                    buffer_img = None

                self._report_progress(
                    "Processing", chunk_count, None, f"Chunk {chunk_count} processed"
                )

        # Handle any remaining buffer content after all images are processed
        if buffer_img is not None and buffer_img.size[1] > 0:
            self._check_cancelled()
            slice_points = self.detector.run(
                buffer_img,
                split_height,
                sensitivity=sensitivity,
                ignorable_pixels=ignorable_pixels,
                scan_step=scan_step,
            )
            for j in range(1, len(slice_points)):
                upper = slice_points[j - 1]
                lower = slice_points[j]
                panel = buffer_img.crop((0, upper, buffer_img.size[0], lower))
                self.img_handler.save(
                    workdirectory, panel, img_iteration, output_type, lossy_quality
                )
                img_iteration += 1

        return workdirectory

    def _check_cancelled(self):
        """Raises CancelledError if cancellation has been requested."""
        if self.cancel_event.is_set():
            raise CancelledError("Process cancelled by user")

    def _report_progress(self, phase, current, total, message):
        """Reports progress via the callback."""
        self.progress_callback(phase, current, total, message)

    def _load_single_image(self, img_path: str) -> pil.Image:
        """Loads a single image, handling PSD/PSB files specially."""
        if os.path.splitext(img_path)[1] not in PHOTOSHOP_FILE_TYPES:
            return pil.open(img_path)
        return PSDImage.open(img_path).topil()

    def _resize_single_image(
        self,
        img: pil.Image,
        enforce_type: WIDTH_ENFORCEMENT,
        target_width: int | None,
    ) -> pil.Image:
        """Resizes a single image based on width enforcement settings."""
        if enforce_type == WIDTH_ENFORCEMENT.NONE:
            return img
        if target_width is None:
            return img
        if img.size[0] == target_width:
            return img
        img_ratio = float(img.size[1] / img.size[0])
        new_height = int(img_ratio * target_width)
        if new_height > 0:
            return img.resize((target_width, new_height), pil.LANCZOS)
        return img

    def _append_to_buffer(self, buffer: pil.Image, img: pil.Image) -> pil.Image:
        """Appends an image to the bottom of the buffer and closes both originals."""
        new_height = buffer.size[1] + img.size[1]
        new_width = max(buffer.size[0], img.size[0])
        combined = pil.new("RGB", (new_width, new_height))
        combined.paste(buffer, (0, 0))
        combined.paste(img, (0, buffer.size[1]))
        buffer.close()
        img.close()
        return combined

    def _resolve_target_width(
        self,
        input_path: str,
        input_files: list[str],
        enforce_type: WIDTH_ENFORCEMENT,
        enforce_width: int,
    ) -> int | None:
        """Resolves the target width based on enforcement mode.
        
        For AUTOMATIC mode, scans all files to find the minimum width.
        """
        if enforce_type == WIDTH_ENFORCEMENT.MANUAL:
            return enforce_width
        if enforce_type == WIDTH_ENFORCEMENT.AUTOMATIC:
            min_width = None
            for img_file in input_files:
                img_path = os.path.join(input_path, img_file)
                with pil.open(img_path) as img:
                    w = img.size[0]
                    if min_width is None or w < min_width:
                        min_width = w
            return min_width
        return None

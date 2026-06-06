import gc
import signal
import threading
from time import time

from core.detectors import select_detector
from core.services import (
    ChunkedProcessor,
    DirectoryExplorer,
    ImageHandler,
    ImageManipulator,
    logFunc,
)
from core.utils.constants import WIDTH_ENFORCEMENT
from core.utils.errors import CancelledError


class ConsoleStitchProcess:
    @logFunc(inclass=True)
    def run(self, kwargs: dict[str:any]):
        # Initialize cancellation event and signal handler for Ctrl+C
        cancel_event = threading.Event()

        def signal_handler(sig, frame):
            print("\nCancelling process...")
            cancel_event.set()

        signal.signal(signal.SIGINT, signal_handler)

        # Initialize Services
        explorer = DirectoryExplorer()
        img_handler = ImageHandler()
        img_manipulator = ImageManipulator()
        detector = select_detector(detection_type=kwargs.get("detection_type"))
        width_enforce_mode = WIDTH_ENFORCEMENT.MANUAL if kwargs.get("custom_width") > 0 else WIDTH_ENFORCEMENT.NONE

        # Starting Stitch Process
        start_time = time()
        print("--- Process Starting Up ---")
        print("Exploring input directory for working directories")
        input_dirs = explorer.run(input=kwargs.get("input_folder"))
        input_dirs_count = len(input_dirs)
        print("[{count}] Working directories were found".format(count=input_dirs_count))

        # Process each working directory
        dir_iteration = 1
        for dir in input_dirs:
            if cancel_event.is_set():
                print("\nProcess cancelled by user.")
                return

            print("-> Starting stitching process for working directory #{iteration} <-".format(iteration=dir_iteration))

            # Initialize and run chunked processor for this directory
            processor = ChunkedProcessor(
                img_handler=img_handler,
                img_manipulator=img_manipulator,
                detector=detector,
                cancel_event=cancel_event,
                progress_callback=lambda phase, current, total, msg: print(
                    "[{iteration}/{count}] {msg}".format(iteration=dir_iteration, count=input_dirs_count, msg=msg)
                ),
            )

            try:
                processor.run(
                    workdirectory=dir,
                    split_height=kwargs.get("split_height"),
                    output_type=kwargs.get("output_type"),
                    lossy_quality=kwargs.get("lossy_quality"),
                    enforce_type=width_enforce_mode,
                    enforce_width=kwargs.get("custom_width"),
                    sensitivity=kwargs.get("detection_senstivity"),
                    ignorable_pixels=kwargs.get("ignorable_pixels"),
                    scan_step=kwargs.get("scan_line_step"),
                )
            except CancelledError:
                print("\nProcess cancelled by user.")
                return

            gc.collect()
            dir_iteration += 1

        # Process completed
        end_time = time()
        print("--- Process completed in {time:.3f} seconds ---".format(time=end_time - start_time))

import gc
import threading
from time import time

from core.detectors import select_detector
from core.services import (
    ChunkedProcessor,
    DirectoryExplorer,
    ImageHandler,
    ImageManipulator,
    PostProcessRunner,
    SettingsHandler,
    logFunc,
)
from core.utils.errors import CancelledError


class GuiStitchProcess:
    @logFunc(inclass=True)
    def run_with_error_msgs(self, **kwargs: dict[str:any]):
        status_func = kwargs.get("status_func", print)
        try:
            return self.run(**kwargs)
        except CancelledError:
            status_func(0, "Idle - Process cancelled by user")
            return None
        except Exception as error:
            status_func(0, "Idle - {0}".format(str(error)))
            raise error

    def run(self, **kwargs: dict[str:any]):
        # Initialize Services
        settings = SettingsHandler()
        explorer = DirectoryExplorer()
        img_handler = ImageHandler()
        img_manipulator = ImageManipulator()
        postprocess_runner = PostProcessRunner()
        detector = select_detector(detection_type=settings.load("detector_type"))

        cancel_event = kwargs.get("cancel_event", threading.Event())
        input_path = kwargs.get("input_path", "")
        output_path = kwargs.get("output_path", "")
        status_func = kwargs.get("status_func", print)
        console_func = kwargs.get("console_func", print)

        has_postprocess = settings.load("run_postprocess")

        # Define step percentages for progress tracking
        step_percentages = {
            "explore": 5.0,
            "process": 75.0,
            "postprocess": 20.0,
        }
        if not has_postprocess:
            step_percentages["process"] = 95.0

        # Starting Stitch Process
        start_time = time()
        percentage = 0.0
        status_func(percentage, "Exploring input directory for working directories")
        input_dirs = explorer.run(input=input_path, output_path=output_path)
        input_dirs_count = len(input_dirs)
        percentage += step_percentages["explore"]
        status_func(
            percentage,
            "[{count}] Working directories were found".format(count=input_dirs_count),
        )

        # Track total images across all directories for progress calculation
        total_images = sum(len(dir.input_files) for dir in input_dirs)
        processed_images = 0

        # Process each working directory
        dir_iteration = 1
        for dir in input_dirs:
            if cancel_event.is_set():
                raise CancelledError("Process cancelled by user")

            dir_image_count = len(dir.input_files)
            dir_percentage_start = percentage
            dir_percentage_range = step_percentages["process"] / input_dirs_count

            status_func(
                percentage,
                "Working - [{iteration}/{count}] Processing images".format(
                    iteration=dir_iteration, count=input_dirs_count
                ),
            )

            # Progress callback for chunked processor
            def progress_callback(phase, current, total, msg):
                nonlocal percentage
                if total_images > 0:
                    progress_in_dir = (processed_images + current) / total_images
                    percentage = (
                        percentage
                        + (dir_percentage_range * progress_in_dir)
                        - (dir_percentage_range * (processed_images / total_images))
                    )
                    percentage = min(
                        percentage,
                        dir_percentage_start + dir_percentage_range,
                    )
                status_func(
                    int(percentage),
                    "Working - [{iteration}/{count}] {msg}".format(
                        iteration=dir_iteration, count=input_dirs_count, msg=msg
                    ),
                )

            # Initialize and run chunked processor for this directory
            processor = ChunkedProcessor(
                img_handler=img_handler,
                img_manipulator=img_manipulator,
                detector=detector,
                cancel_event=cancel_event,
                progress_callback=progress_callback,
            )

            processor.run(
                workdirectory=dir,
                split_height=settings.load("split_height"),
                output_type=settings.load("output_type"),
                lossy_quality=settings.load("lossy_quality"),
                enforce_type=settings.load("enforce_type"),
                enforce_width=settings.load("enforce_width"),
                sensitivity=settings.load("senstivity"),
                ignorable_pixels=settings.load("ignorable_pixels"),
                scan_step=settings.load("scan_step"),
            )

            processed_images += dir_image_count
            percentage = dir_percentage_start + dir_percentage_range
            gc.collect()

            # Run postprocess if enabled
            if settings.load("run_postprocess"):
                status_func(
                    int(percentage),
                    "Working - [{iteration}/{count}] Running post process on output files".format(
                        iteration=dir_iteration,
                        count=input_dirs_count,
                    ),
                )
                postprocess_runner.run(
                    workdirectory=dir,
                    postprocess_app=settings.load("postprocess_app"),
                    postprocess_args=settings.load("postprocess_args"),
                    console_func=console_func,
                )
                percentage += step_percentages["postprocess"] / input_dirs_count

            dir_iteration += 1

        # Process completed
        end_time = time()
        percentage = 100
        status_func(
            percentage,
            "Idle - Process completed in {time:.3f} seconds".format(time=end_time - start_time),
        )

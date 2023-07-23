import gc
import subprocess
from time import time

from core.detectors import select_detector
from core.services import (
    DirectoryExplorer,
    ImageHandler,
    ImageManipulator,
    PostProcessRunner,
    SettingsHandler,
    logFunc,
)


class GuiStitchProcess:
    @logFunc(inclass=True)
    def run_with_error_msgs(self, **kwargs: dict[str, any]):
        # Function to run the stitching process with error handling
        # It logs any errors and re-raises them after displaying the error message.
        status_func = kwargs.get("status_func", print)
        try:
            return self.run(**kwargs)
        except Exception as error:
            status_func(0, "Idle - {0}".format(str(error)))
            raise error

    def run(self, **kwargs: dict[str, any]):
        # Main function to run the stitching process
        # It combines and slices images from input directories and saves them to the output directory.

        # Initialize Services
        settings = SettingsHandler()
        explorer = DirectoryExplorer()
        img_handler = ImageHandler()
        img_manipulator = ImageManipulator()
        postprocess_runner = PostProcessRunner()
        detector = select_detector(detection_type=settings.load("detector_type"))
        input_path = kwargs.get("input_path", "")
        output_path = kwargs.get("output_path", "")
        status_func = kwargs.get("status_func", print)
        console_func = kwargs.get("console_func", print)
        use_waifu2x = kwargs.get("use_waifu2x", False)

        # Define step percentages for progress tracking
        step_percentages = {
            "explore": 5.0,
            "load": 15.0,
            "combine": 5.0,
            "detect": 15.0,
            "slice": 10.0,
            "save": 30.0,
            "postprocess": 20.0,
        }

        # Check if post-processing is enabled in settings
        has_postprocess = settings.load("run_postprocess")
        if not has_postprocess:
            # If post-processing is disabled, allocate more progress percentage to the "save" step.
            step_percentages["save"] = 50.0

        # Starting Stitch Process
        start_time = time()
        percentage = 0.0
        status_func(percentage, "Exploring input directory for working directories")
        # Explore input directory to find working directories
        if use_waifu2x:
            input_dirs = explorer.run(input=input_path, output_path=output_path + "/tmp")
        else:
            input_dirs = explorer.run(input=input_path, output_path=output_path)
        print(input_dirs)
        input_dirs_count = len(input_dirs)
        status_func(
            percentage,
            "Working - [{count}] Working directories were found".format(
                count=input_dirs_count
            ),
        )
        percentage += step_percentages.get("explore")

        dir_iteration = 1
        for dir in input_dirs:
            # Process each working directory one by one
            status_func(
                percentage,
                "Working - [{iteration}/{count}] Preparing & loading images Into memory".format(
                    iteration=dir_iteration, count=input_dirs_count
                ),
            )

            # Load images from the current working directory
            imgs = img_handler.load(dir)
            # Resize images based on specified settings
            imgs = img_manipulator.resize(
                imgs,
                settings.load("enforce_type"),
                settings.load("enforce_width"),
            )
            percentage += step_percentages.get("load") / float(input_dirs_count)
            status_func(
                percentage,
                "Working - [{iteration}/{count}] Combining images into a single combined image".format(
                    iteration=dir_iteration, count=input_dirs_count
                ),
            )
            # Combine images into a single image
            combined_img = img_manipulator.combine(imgs)
            percentage += step_percentages.get("combine") / float(input_dirs_count)
            status_func(
                percentage,
                "Working - [{iteration}/{count}] Detecting & selecting valid slicing points".format(
                    iteration=dir_iteration, count=input_dirs_count
                ),
            )
            # Detect valid slicing points in the combined image
            slice_points = detector.run(
                combined_img,
                settings.load("split_height"),
                sensitivity=settings.load("senstivity"),
                ignorable_pixels=settings.load("ignorable_pixels"),
                scan_step=settings.load("scan_step"),
            )
            percentage += step_percentages.get("detect") / float(input_dirs_count)
            status_func(
                percentage,
                "Working - [{iteration}/{count}] Generating sliced output images in memory".format(
                    iteration=dir_iteration, count=input_dirs_count
                ),
            )
            # Generate sliced output images based on the detected points
            imgs = img_manipulator.slice(combined_img, slice_points)
            percentage += step_percentages.get("slice") / float(input_dirs_count)
            status_func(
                percentage,
                "Working - [{iteration}/{count}] Saving output images to storage".format(
                    iteration=dir_iteration, count=input_dirs_count
                ),
            )
            img_iteration = 1
            img_count = len(imgs)
            for img in imgs:
                # Save each sliced image to the temporary directory if use_waifu2x is True
                if use_waifu2x:
                    img_file_name = img_handler.save(
                        dir,
                        img,
                        img_iteration,
                        img_format=settings.load("output_type"),
                        quality=settings.load("lossy_quality"),
                    )
                else:
                    img_file_name = img_handler.save(
                        dir,
                        img,
                        img_iteration,
                        img_format=settings.load("output_type"),
                        quality=settings.load("lossy_quality"),
                    )
                img_iteration += 1
                percentage += step_percentages.get("save") / (
                    float(input_dirs_count) * float(img_count)
                )
                status_func(
                    percentage,
                    "Working - [{iteration}/{count}] {file} has been successfully saved".format(
                        iteration=dir_iteration,
                        count=input_dirs_count,
                        file=img_file_name,
                    ),
                )
            # Perform garbage collection to free up memory after processing a directory
            gc.collect()
            if settings.load("run_postprocess"):
                # If post-processing is enabled, run the post-processing step
                status_func(
                    percentage,
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
                percentage += step_percentages.get("postprocess") / (
                    float(input_dirs_count) * float(img_count)
                )
            dir_iteration += 1

        if use_waifu2x:
            # Run waifu2x_path with specified parameters
            percentage = 95
            status_func(
                percentage,
                "Waifu2x-Caffe is processing"
            )
            waifu2x_path = kwargs.get("waifu2x_path", "")
            if waifu2x_path:
                # Construct the command for waifu2x_path
                command = [
                    waifu2x_path,
                    "-i",
                    output_path + "/tmp",
                    "-o",
                    output_path,
                    "-m",
                    kwargs.get("mode", "noise_scale"),
                    "-s",
                    str(kwargs.get("scale_ratio", 2.0)),
                    "-n",
                    str(kwargs.get("noise_level", 0)),
                    "-p",
                    "cudnn",
                    "-c",
                    str(kwargs.get("crop_size", 128)),
                    "-q",
                    str(kwargs.get("output_quality", -1)),
                    "-d",
                    str(kwargs.get("output_depth", 8)),
                    "-b",
                    str(kwargs.get("batch_size", 1)),
                    "--gpu",
                    str(kwargs.get("gpu_device", 0)),
                    "-t",
                    str(kwargs.get("tta", 0)),
                    "--model_dir",
                    str("models/" + kwargs.get("profile", "cunet")),
                ]

                # Run the waifu2x_path command
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                end_time = time()
                percentage = 100
                status_func(
                    percentage,
                    "Idle - Process completed in {time:.3f} seconds".format(
                        time=end_time - start_time
                    ),
                )
        else:
            end_time = time()
            percentage = 100
            status_func(
                percentage,
                "Idle - Process completed in {time:.3f} seconds".format(
                    time=end_time - start_time
                ),
            )

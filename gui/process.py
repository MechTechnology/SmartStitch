import gc
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
    def run_with_error_msgs(self, **kwargs: dict[str:any]):
        status_func = kwargs.get("status_func", print)
        try:
            return self.run(**kwargs)
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
        input_path = kwargs.get("input_path", "")
        output_path = kwargs.get("input_path", "")
        status_func = kwargs.get("status_func", print)
        console_func = kwargs.get("console_func", print)
        step_percentages = {
            "explore": 5.0,
            "load": 15.0,
            "combine": 5.0,
            "detect": 15.0,
            "slice": 10.0,
            "save": 30.0,
            "postprocess": 20.0,
        }
        has_postprocess = settings.load("run_postprocess")
        if not has_postprocess:
            step_percentages["save"] = 50.0

        # Starting Stitch Process
        start_time = time()
        percentage = 0.0
        status_func(percentage, 'Exploring input directory for working directories')
        input_dirs = explorer.run(input=input_path, output_path=output_path)
        input_dirs_count = len(input_dirs)
        status_func(
            percentage,
            'Working - [{count}] Working directories were found'.format(
                count=input_dirs_count
            ),
        )
        percentage += step_percentages.get("explore")
        dir_iteration = 1
        for dir in input_dirs:
            status_func(
                percentage,
                'Working - [{iteration}/{count}] Preparing & loading images Into memory'.format(
                    iteration=dir_iteration, count=input_dirs_count
                ),
            )
            imgs = img_handler.load(dir)
            imgs = img_manipulator.resize(
                imgs, settings.load("enforce_type"), settings.load("enforce_width")
            )
            percentage += step_percentages.get("load") / float(input_dirs_count)
            status_func(
                percentage,
                'Working - [{iteration}/{count}] Combining images into a single combined image'.format(
                    iteration=dir_iteration, count=input_dirs_count
                ),
            )
            combined_img = img_manipulator.combine(imgs)
            percentage += step_percentages.get("combine") / float(input_dirs_count)
            status_func(
                percentage,
                'Working - [{iteration}/{count}] Detecting & selecting valid slicing points'.format(
                    iteration=dir_iteration, count=input_dirs_count
                ),
            )
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
                'Working - [{iteration}/{count}] Generating sliced output images in memory'.format(
                    iteration=dir_iteration, count=input_dirs_count
                ),
            )
            imgs = img_manipulator.slice(combined_img, slice_points)
            percentage += step_percentages.get("slice") / float(input_dirs_count)
            status_func(
                percentage,
                'Working - [{iteration}/{count}] Saving output images to storage'.format(
                    iteration=dir_iteration, count=input_dirs_count
                ),
            )
            img_iteration = 1
            img_count = len(imgs)
            for img in imgs:
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
                    'Working - [{iteration}/{count}] {file} has been successfully saved'.format(
                        iteration=dir_iteration,
                        count=input_dirs_count,
                        file=img_file_name,
                    ),
                )
            gc.collect()
            if settings.load("run_postprocess"):
                status_func(
                    percentage,
                    'Working - [{iteration}/{count}] Running post process on output files'.format(
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
        end_time = time()
        percentage = 100
        status_func(
            percentage,
            'Idle - Process completed in {time:.3f} seconds'.format(
                time=end_time - start_time
            ),
        )

import gc
from time import time

from core.detectors import select_detector
from core.services import (
    DirectoryExplorer,
    ImageHandler,
    ImageManipulator,
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
        detector = select_detector(detection_type=settings.load("detector_type"))
        input_path = kwargs.get("input_path", "")
        output_path = kwargs.get("input_path", "")
        status_func = kwargs.get("status_func", print)

        # Starting Stitch Process
        start_time = time()
        percentage = 0
        status_func(percentage, 'Exploring input directory for working directories')
        input_dirs = explorer.run(input=input_path, output_path=output_path)
        input_dirs_count = len(input_dirs)
        status_func(
            percentage,
            'Working - [{count}] Working directories were found'.format(
                count=input_dirs_count
            ),
        )
        percentage += 5
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
            percentage += 15.0 / float(input_dirs_count)
            status_func(
                percentage,
                'Working - [{iteration}/{count}] Combining images into a single combined image'.format(
                    iteration=dir_iteration, count=input_dirs_count
                ),
            )
            combined_img = img_manipulator.combine(imgs)
            percentage += 5.0 / float(input_dirs_count)
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
            percentage += 15.0 / float(input_dirs_count)
            status_func(
                percentage,
                'Working - [{iteration}/{count}] Generating sliced output images in memory'.format(
                    iteration=dir_iteration, count=input_dirs_count
                ),
            )
            imgs = img_manipulator.slice(combined_img, slice_points)
            percentage += 10.0 / float(input_dirs_count)
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
                percentage += 50.0 / (float(input_dirs_count) * float(img_count))
                status_func(
                    percentage,
                    'Working - [{iteration}/{count}] {file} has been successfully saved'.format(
                        iteration=dir_iteration,
                        count=input_dirs_count,
                        file=img_file_name,
                    ),
                )
            dir_iteration += 1
            gc.collect()
        end_time = time()
        percentage = 100
        status_func(
            percentage,
            'Idle - Process completed in {time:.3f} seconds'.format(
                time=end_time - start_time
            ),
        )

import gc
from time import time

from core.detectors import select_detector
from core.services import DirectoryExplorer, ImageHandler, ImageManipulator, logFunc
from core.utils.constants import WIDTH_ENFORCEMENT


# Define a class to handle the console stitch process
class ConsoleStitchProcess:
    @logFunc(inclass=True)
    def run(self, kwargs: dict[str:any]):
        """
        Main method to run the console stitch process.

        :param kwargs: A dictionary containing the input arguments for the process.
        """

        # Initialize Services
        explorer = DirectoryExplorer()
        img_handler = ImageHandler()
        img_manipulator = ImageManipulator()
        detector = select_detector(detection_type=kwargs.get('detection_type'))

        # Determine whether manual width enforcement is needed
        width_enforce_mode = (
            WIDTH_ENFORCEMENT.MANUAL
            if kwargs.get('custom_width') > 0
            else WIDTH_ENFORCEMENT.NONE
        )

        # Starting Stitch Process
        start_time = time()
        print('--- Process Starting Up ---')

        # Explore input directory for working directories
        print('Exploring input directory for working directories')
        input_dirs = explorer.run(input=kwargs.get("input_folder"))
        input_dirs_count = len(input_dirs)
        print('[{count}] Working directories were found'.format(count=input_dirs_count))
        dir_iteration = 1

        # Iterate over each working directory
        for dir in input_dirs:
            print(
                '-> Starting stitching process for working directory #{iteration} <-'.format(
                    iteration=dir_iteration
                )
            )

            # Load and prepare images into memory
            print(
                '[{iteration}/{count}] Preparing & loading images Into memory'.format(
                    iteration=dir_iteration, count=input_dirs_count
                )
            )
            imgs = img_handler.load(dir)
            imgs = img_manipulator.resize(
                imgs, width_enforce_mode, kwargs.get('custom_width')
            )

            # Combine images into a single combined image
            print(
                '[{iteration}/{count}] Combining images into a single combined image'.format(
                    iteration=dir_iteration, count=input_dirs_count
                )
            )
            combined_img = img_manipulator.combine(imgs)

            # Detect and select valid slicing points
            print(
                '[{iteration}/{count}] Detecting & selecting valid slicing points'.format(
                    iteration=dir_iteration, count=input_dirs_count
                )
            )
            slice_points = detector.run(
                combined_img,
                kwargs.get("split_height"),
                sensitivity=kwargs.get("detection_senstivity"),
                ignorable_pixels=kwargs.get("ignorable_pixels"),
                scan_step=kwargs.get("scan_line_step"),
            )

            # Generate sliced output images in memory
            print(
                '[{iteration}/{count}] Generating sliced output images in memory'.format(
                    iteration=dir_iteration, count=input_dirs_count
                )
            )
            imgs = img_manipulator.slice(combined_img, slice_points)

            # Save output images to storage
            print(
                '[{iteration}/{count}] Saving output images to storage'.format(
                    iteration=dir_iteration, count=input_dirs_count
                )
            )
            img_iteration = 1
            for img in imgs:
                img_file_name = img_handler.save(
                    dir,
                    img,
                    img_iteration,
                    img_format=kwargs.get("output_type"),
                    quality=kwargs.get('lossy_quality'),
                )
                img_iteration += 1
                print(
                    '[{iteration}/{count}] {file} has been successfully saved'.format(
                        iteration=dir_iteration,
                        count=input_dirs_count,
                        file=img_file_name,
                    )
                )

            dir_iteration += 1
            # Perform garbage collection to free up memory
            gc.collect()

        end_time = time()
        print(
            '--- Process completed in {time:.3f} seconds ---'.format(
                time=end_time - start_time
            )
        )
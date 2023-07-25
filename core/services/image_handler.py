import os
from PIL import Image as pil
from psd_tools import PSDImage
from ..models import WorkDirectory
from .global_logger import logFunc
from ..utils.constants import PHOTOSHOP_FILE_TYPES

class ImageHandler:
    @logFunc(inclass=True)
    def load(self, workdirectory: WorkDirectory) -> list[pil.Image]:
        """Loads all image files in a given work into a list of PIL image objects."""
        img_objs = []
        # Loop through each image file in the input_files list of the work directory
        for imgFile in workdirectory.input_files:
            # Create the full path to the image file
            imgPath = os.path.join(workdirectory.input_path, imgFile)
            # Check if the file is not a Photoshop file based on its extension
            if os.path.splitext(imgPath)[1] not in PHOTOSHOP_FILE_TYPES:
                # If it's not a Photoshop file, open the image using PIL and add it to the list
                image = pil.open(imgPath)
            else:
                # If it's a Photoshop file, open it using psd_tools and convert it to a PIL image
                image = PSDImage.open(imgPath).topil()
            img_objs.append(image)
        return img_objs

    @logFunc(inclass=True)
    def save(
        self,
        workdirectory: WorkDirectory,
        img_obj: pil.Image,
        img_iteration: int,
        img_format: str = '.png',
        quality: int = 100,
    ) -> str:
        """Saves a single image object to the output path with a specified format and quality."""
        # Create the output directory if it doesn't exist
        os.makedirs(workdirectory.output_path, exist_ok=True)
        
        # Generate the filename for the image using the img_iteration number and img_format
        img_file_name = f'{img_iteration:02}{img_format}'
        
        if img_format in PHOTOSHOP_FILE_TYPES:
            # If the output format is a Photoshop format, convert the PIL image to a PSDImage
            psd_obj = PSDImage.frompil(img_obj)
            # Save the PSDImage to the output path
            psd_obj.save(os.path.join(workdirectory.output_path, img_file_name))
        else:
            # If the output format is not a Photoshop format, save the PIL image with the specified quality
            img_obj.save(
                os.path.join(workdirectory.output_path, img_file_name),
                quality=quality,
            )
            # Close the PIL image after saving
            img_obj.close()
        
        # Add the filename to the list of output_files in the work directory
        workdirectory.output_files.append(img_file_name)
        return img_file_name

    def save_all(
        self,
        workdirectory: WorkDirectory,
        img_objs: list[pil.Image],
        img_format: str = '.png',
        quality: int = 100,
    ) -> WorkDirectory:
        """Saves all image objects in the img_objs list to the output path with the specified format and quality."""
        img_iteration = 1
        # Iterate through each image object in the list and save it using the save method
        for img in img_objs:
            self.save(workdirectory, img, img_iteration, img_format, quality)
            img_iteration += 1
        return workdirectory
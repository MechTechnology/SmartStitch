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
        for imgFile in workdirectory.input_files:
            imgPath = os.path.join(workdirectory.input_path, imgFile)
            if os.path.splitext(imgPath)[1] not in PHOTOSHOP_FILE_TYPES:
                image = pil.open(imgPath)
            else:
                image = PSDImage.open(imgPath).topil()
            img_objs.append(image)
        return img_objs

    @logFunc(inclass=True)
    def save(
        self,
        workdirectory: WorkDirectory,
        img_obj: pil.Image,
        img_iteration: 1,
        img_format: str = '.png',
        quality=100,
    ) -> str:
        if not os.path.exists(workdirectory.output_path):
            os.makedirs(workdirectory.output_path)
        img_file_name = str(f'{img_iteration:02}') + img_format
        if img_format in PHOTOSHOP_FILE_TYPES:
            psd_obj = PSDImage.frompil(img_obj)
            psd_obj.save(
                workdirectory.output_path + '/' + img_file_name,
            )
        else:
            img_obj.save(
                workdirectory.output_path + '/' + img_file_name,
                quality=quality,
            )
            img_obj.close()
        workdirectory.output_files.append(img_file_name)
        return img_file_name

    def save_all(
        self,
        workdirectory: WorkDirectory,
        img_objs: list[pil.Image],
        img_format: str = '.png',
        quality=100,
    ) -> WorkDirectory:
        img_iteration = 1
        for img in img_objs:
            self.save(workdirectory, img, img_iteration, img_format, quality)
            img_iteration += 1
        return workdirectory

from os import makedirs, path
from typing import List
from PIL import Image as pil
from core.models.work_directory import WorkDirectory
from core.services.global_logger import logFunc

class ImageHandler():
  @logFunc(inclass=True)
  def load(self, workdirectory: WorkDirectory) -> List[pil.Image]:
    """Loads all image files in a given work into a list of PIL image objects."""
    img_objs = []
    for imgFile in workdirectory.input_files:
      imgPath = path.join(workdirectory.input_path, imgFile)
      image = pil.open(imgPath)
      img_objs.append(image)
    return img_objs
  
  @logFunc(inclass=True)
  def save(self, workdirectory: WorkDirectory, img_objs: List[pil.Image], img_format: str='.jpg') -> WorkDirectory:
    if not path.exists(workdirectory.output_path):
      makedirs(workdirectory.output_path)
    img_index = 1
    for img in img_objs:
      img.save(workdirectory.output_path + '/' + str(f'{img_index:02}') + img_format, quality=100)
      workdirectory.output_files.append(str(f'{img_index:02}') + img_format)
      img_index += 1
    return workdirectory
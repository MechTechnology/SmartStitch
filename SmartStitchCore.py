from PIL import ImageFile, Image as pil
from natsort import natsorted
import numpy as np
import os
import subprocess
ImageFile.LOAD_TRUNCATED_IMAGES = True

def get_folder_paths(batch_mode_enabled, given_input_folder, given_output_folder):
  """Gets paths of all input and output folders."""
  folder_paths = []
  given_input_folder = os.path.abspath(given_input_folder)
  given_output_folder = os.path.abspath(given_output_folder)
  if batch_mode_enabled == False:
    folder_paths.append((given_input_folder, given_output_folder))
  else:
    # Gets Absolute paths to the folders within the given path
    for fileName in os.listdir(given_input_folder):
      filePath = os.path.join(given_input_folder, fileName)
      if os.path.isdir(filePath):
        folder_paths.append((filePath, os.path.join(given_output_folder, fileName + " [Stitched]")))
  return folder_paths

def load_images(foldername):
  """Loads all image files in a given folder into a list of pillow image objects."""
  images = []
  if (foldername == ""):
    return images
  folder = os.path.abspath(str(foldername))
  files = natsorted(os.listdir(folder))
  if len(files) == 0:
    return images
  for imgFile in files:
    if imgFile.lower().endswith(('.png', '.webp', '.jpg', '.jpeg', '.jfif', '.bmp', '.tiff', '.tga')):
      imgPath = os.path.join(folder, imgFile)
      image = pil.open(imgPath)
      images.append(image)
  return images

def resize_images(images, width_enforce_type, custom_width=720):
  """Resizes the images according to what enforcement mode you have."""
  enforce_type = width_enforce_type
  if width_enforce_type == 0:
    return images
  else:
    resized_images = []
    new_image_width = 0
    if width_enforce_type == 1:
      widths, heights = zip(*(image.size for image in images))
      new_image_width = min(widths)
    elif width_enforce_type == 2:
      new_image_width = int(custom_width)
    for image in images:
      if image.size[0] == new_image_width:
        resized_images.append(image)
      else:
        ratio = float(image.size[1] / image.size[0])
        new_image_height = int(ratio * new_image_width)
        new_image = image.resize((new_image_width, new_image_height), pil.ANTIALIAS)
        resized_images.append(new_image)
    return resized_images

def combine_images(images):
  """All this does is combine all the files into a single image in the memory."""
  widths, heights = zip(*(image.size for image in images))
  new_image_width = max(widths)
  new_image_height = sum(heights)
  new_image = pil.new('RGB', (new_image_width, new_image_height))
  combine_offset = 0
  for image in images:
      new_image.paste(image, (0, combine_offset))
      combine_offset += image.size[1]
  return new_image


def adjust_split_location(combined_pixels, split_height, split_offset, senstivity, ignorable_pixels, scan_step):
  """Where the smart magic happens, compares pixels of each row, to decide if it's okay to cut there."""
  threshold = int(255 * (1-(senstivity/100)))
  adjust_in_progress = True
  new_split_height = split_height
  last_row = len(combined_pixels) - 1
  split_row = split_offset + new_split_height
  countdown = True
  while (adjust_in_progress and split_row < last_row):
    adjust_in_progress = False
    split_row = split_offset + new_split_height
    pixel_row = combined_pixels[split_row]
    prev_pixel = int(pixel_row[ignorable_pixels])
    for x in range((ignorable_pixels+1), len(pixel_row)-(ignorable_pixels)):
      current_pixel = int(pixel_row[x])
      pixel_value_diff = current_pixel - prev_pixel
      if (pixel_value_diff < -threshold or pixel_value_diff > threshold):
        if (countdown):
          new_split_height -= scan_step
        else:
          new_split_height += scan_step
        adjust_in_progress = True
        break
      current_pixel = prev_pixel
    if (new_split_height < 0.5*split_height):
      new_split_height = split_height
      countdown = False
      adjust_in_progress = True
  return new_split_height

def split_image(combined_img, split_height, senstivity, ignorable_pixels, scan_step):
  """Splits the gaint combined img into small images passed on desired height."""
  split_height = int(split_height)
  senstivity = int(senstivity)
  ignorable_pixels = int(ignorable_pixels)
  scan_step = int(scan_step)
  max_width = combined_img.size[0]
  max_height = combined_img.size[1]
  combined_pixels = np.array(combined_img.convert('L'))
  images = []
  # The spliting starts here (calls another function to decide where to slice)
  split_offset = 0
  while((split_offset + split_height) < max_height):
    new_split_height = adjust_split_location(combined_pixels, split_height, split_offset, senstivity, ignorable_pixels, scan_step)
    split_image = pil.new('RGB', (max_width, new_split_height))
    split_image.paste(combined_img,(0,-split_offset))
    split_offset += new_split_height
    images.append(split_image)
  # Final image (What ever is remaining in the combined img, will be smaller than the rest for sure)
  remaining_rows = max_height-split_offset
  if (remaining_rows > 0):
    split_image = pil.new('RGB', (max_width, max_height-split_offset))
    split_image.paste(combined_img,(0,-split_offset))
    images.append(split_image)
  return images

def save_data(data, foldername, outputformat, progress_func = None):
  """Saves the given images/date in the output folder."""
  new_folder = str(foldername)
  if not os.path.exists(new_folder):
    os.makedirs(new_folder)
  imageIndex = 1
  for image in data:
    if (progress_func != None):
      progress_func(len(data))
    image.save(new_folder + '/' + str(f'{imageIndex:02}') + outputformat, quality=100)
    imageIndex += 1
  return

def call_external_func(cmd, display_output, processed_path):
  if not os.path.exists(processed_path) and '[Processed]' in cmd:
    os.makedirs(processed_path)
  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
  display_output("Subprocess started!\n")
  for line in proc.stdout:
    display_output(line)
  for line in proc.stderr:
    display_output(line)
  display_output("\nSubprocess finished successfully!\n")
  proc.stdout.close()
  return_code = proc.wait()
  if return_code:
    raise subprocess.CalledProcessError(return_code, cmd)
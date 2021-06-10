# Smart Stitchy By MechTechnology
# How to you use:
# 1. Put your raws in folders in the same directory as this script
# 2. Go the very end of this script and add a call to the function
# SaveSplitVertical(Foldername, AverageImgHeight, Senstivity)
# Example if i put my raw in a folder called Chapter 40 and want them to be 4300 height on average (90% is a good senstivity)
# SaveSplitVertical(Chapter 40, 4300, 90)
# output will be in the (foldername + [Stitched])
#
# that is all, you can add multiple calls to different folder to do bigger batchs at once

from PIL import Image as pil
import numpy as np
import os

def LoadImages(folder):
    images = []
    for imgFile in os.listdir(folder):
        imgPath = folder + '/' + imgFile
        image = pil.open(imgPath)
        if image is not None:
            images.append(image)
    return images

def CombineVertically(folder):
    images = LoadImages(folder)
    
    widths, heights = zip(*(image.size for image in images))
    new_image_width = max(widths)
    new_image_height = sum(heights)
    new_image = pil.new('RGB', (new_image_width, new_image_height))

    combine_offset = 0
    for image in images:
        new_image.paste(image, (0, combine_offset))
        combine_offset += image.size[1]
    return new_image

def SmartAdjust(combined_pixels, split_height, split_offset, senstivity):
    AdjustSensitivity = int(255 * (1-(senstivity/100)))
    adjust_in_progress = True
    new_split_height = split_height
    countdown = True
    while (adjust_in_progress):
        adjust_in_progress = False
        split_row = split_offset + new_split_height
        pixel_row = combined_pixels[split_row]
        prev_pixel = pixel_row[0]
        for x in range(1, len(pixel_row)):
            current_pixel = pixel_row[x]
            diff_pixel = current_pixel - prev_pixel
            if (diff_pixel > AdjustSensitivity):
                if (countdown):
                    new_split_height -= 1
                else:
                    new_split_height += 1
                adjust_in_progress = True
                break
            current_pixel = prev_pixel
        if (new_split_height < 0.5*split_height):
            new_split_height = split_height
            countdown = False
            adjust_in_progress = True
    return new_split_height


def SplitVertical(folder, split_height, senstivity=90):
    combined_img = CombineVertically(folder)
    max_width = combined_img.size[0]
    max_height = combined_img.size[1]
    combined_pixels = np.array(combined_img.convert('L'))
    images = []
    split_offset = 0
    while((split_offset + split_height) < max_height):
        new_split_height = SmartAdjust(combined_pixels, split_height, split_offset, senstivity)
        split_image = pil.new('RGB', (max_width, new_split_height))
        split_image.paste(combined_img,(0,-split_offset))
        split_offset += new_split_height
        images.append(split_image)
    
    #Final image
    split_image = pil.new('RGB', (max_width, max_height-split_offset))
    split_image.paste(combined_img,(0,-split_offset))
    images.append(split_image)

    print("Number of Output Page:", len(images))
    return images

def SaveData(folder, data, single_file = False):
    new_folder = folder + " [Stitched]"
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    
    if (single_file):
        data.save(new_folder + '/Combined.png')
        return

    imageIndex = 1
    for image in data:
        image.save(new_folder + '/' + str(f'{imageIndex:02}') + '.png')
        imageIndex += 1
    return

def SaveSplitVertical(folder, split_height, senstivity=90):
    data = SplitVertical(folder, split_height, senstivity)
    SaveData(folder, data)
    print("Files Successfully Stitched!")


#Here Just Call SaveSplitVertical(Foldername, AverageImgHeight, Senstivity)
SaveSplitVertical("Chapter 40", 4300, 90)

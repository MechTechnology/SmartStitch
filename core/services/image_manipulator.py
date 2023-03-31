from PIL import Image as pil

from ..utils.constants import WIDTH_ENFORCEMENT
from .global_logger import logFunc


class ImageManipulator:
    @logFunc(inclass=True)
    def resize(
        self,
        img_objs: list[pil.Image],
        enforce_setting: WIDTH_ENFORCEMENT,
        custom_width: int = 720,
    ) -> list[pil.Image]:
        """Resizes all given images according to the set enforcement setting."""
        if enforce_setting == WIDTH_ENFORCEMENT.NONE:
            return img_objs
        # Resizing Image Logic depending on enforcement settings
        resized_imgs = []
        new_img_width = 0
        if enforce_setting == WIDTH_ENFORCEMENT.AUTOMATIC:
            widths, heights = zip(*(img.size for img in img_objs))
            new_img_width = min(widths)
        elif enforce_setting == WIDTH_ENFORCEMENT.MANUAL:
            new_img_width = custom_width
        for img in img_objs:
            if img.size[0] == new_img_width:
                resized_imgs.append(img)
                continue
            img_ratio = float(img.size[1] / img.size[0])
            new_img_height = int(img_ratio * new_img_width)
            if new_img_height > 0:
                img = img.resize((new_img_width, new_img_height), pil.ANTIALIAS)
                resized_imgs.append(img)
        return resized_imgs

    @logFunc(inclass=True)
    def combine(self, img_objs: list[pil.Image]) -> pil.Image:
        """Combines given image objs to a single vertically stacked single image obj."""
        widths, heights = zip(*(img.size for img in img_objs))
        combined_img_width = max(widths)
        combined_img_height = sum(heights)
        combined_img = pil.new('RGB', (combined_img_width, combined_img_height))
        combine_offset = 0
        for img in img_objs:
            combined_img.paste(img, (0, combine_offset))
            combine_offset += img.size[1]
            img.close()
        return combined_img

    @logFunc(inclass=True)
    def slice(
        self, combined_img: pil.Image, slice_locations: list[int]
    ) -> list[pil.Image]:
        """Combines given combined img to into multiple img slices given the slice locations."""
        max_width = combined_img.size[0]
        img_objs = []
        for index in range(1, len(slice_locations)):
            upper_limit = slice_locations[index - 1]
            lower_limit = slice_locations[index]
            slice_boundaries = (0, upper_limit, max_width, lower_limit)
            img_slice = combined_img.crop(slice_boundaries)
            img_objs.append(img_slice)
        combined_img.close()
        return img_objs

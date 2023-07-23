from PIL import Image as pil
from ..utils.constants import WIDTH_ENFORCEMENT
from .global_logger import logFunc

# Define a class for image manipulation
class ImageManipulator:
    # Decorator logFunc is used to log function calls with inclass=True indicating it's a class method
    @logFunc(inclass=True)
    def resize(
        self,
        img_objs: list[pil.Image],
        enforce_setting: WIDTH_ENFORCEMENT,
        custom_width: int = 720,
    ) -> list[pil.Image]:
        """Resizes all given images according to the set enforcement setting."""
        # If no enforcement is required, return the original images
        if enforce_setting == WIDTH_ENFORCEMENT.NONE:
            return img_objs

        # Initialize a list to store resized images
        resized_imgs = []
        new_img_width = 0

        # Check the enforcement setting and calculate the new image width accordingly
        if enforce_setting == WIDTH_ENFORCEMENT.AUTOMATIC:
            # If automatic, set the new width to the minimum width among the input images
            widths, heights = zip(*(img.size for img in img_objs))
            new_img_width = min(widths)
        elif enforce_setting == WIDTH_ENFORCEMENT.MANUAL:
            # If manual, use the custom width provided
            new_img_width = custom_width

        # Loop through each image and resize it if needed
        for img in img_objs:
            if img.size[0] == new_img_width:
                # If the image width matches the new width, no need to resize, add it to the list
                resized_imgs.append(img)
                continue
            # Calculate the new height while preserving the aspect ratio
            img_ratio = float(img.size[1] / img.size[0])
            new_img_height = int(img_ratio * new_img_width)
            if new_img_height > 0:
                # Resize the image using the calculated new width and height
                img = img.resize((new_img_width, new_img_height), pil.ANTIALIAS)
                resized_imgs.append(img)

        # Return the list of resized images
        return resized_imgs

    # Decorator logFunc is used to log function calls with inclass=True indicating it's a class method
    @logFunc(inclass=True)
    def combine(self, img_objs: list[pil.Image]) -> pil.Image:
        """Combines given image objs to a single vertically stacked single image obj."""
        # Calculate the width and height of the combined image
        widths, heights = zip(*(img.size for img in img_objs))
        combined_img_width = max(widths)
        combined_img_height = sum(heights)

        # Create a new empty image to combine the input images
        combined_img = pil.new('RGB', (combined_img_width, combined_img_height))

        # Combine the images vertically with an offset based on each image's height
        combine_offset = 0
        for img in img_objs:
            combined_img.paste(img, (0, combine_offset))
            combine_offset += img.size[1]
            img.close()

        # Return the combined image
        return combined_img

    # Decorator logFunc is used to log function calls with inclass=True indicating it's a class method
    @logFunc(inclass=True)
    def slice(
        self, combined_img: pil.Image, slice_locations: list[int]
    ) -> list[pil.Image]:
        """Combines given combined img into multiple img slices given the slice locations."""
        # Get the maximum width of the combined image
        max_width = combined_img.size[0]

        # Initialize a list to store the image slices
        img_objs = []

        # Loop through each slice location and extract the corresponding image slice
        for index in range(1, len(slice_locations)):
            upper_limit = slice_locations[index - 1]
            lower_limit = slice_locations[index]
            slice_boundaries = (0, upper_limit, max_width, lower_limit)
            img_slice = combined_img.crop(slice_boundaries)
            img_objs.append(img_slice)

        # Close the original combined image (free up memory)
        combined_img.close()

        # Return the list of image slices
        return img_objs
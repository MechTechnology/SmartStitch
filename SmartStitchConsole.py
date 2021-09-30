import SmartStitchCore as ssc

def run_stitch_process(input_folder, split_height, output_files_type, batch_mode=False, width_enforce_type=0, custom_width=720, senstivity=90, ignorable_pixels=0, scan_line_step=5):
  """Runs the stitch process using the SS core functions, and updates the progress on the UI."""
  output_folder = input_folder + " [Stitched]"
  print("Working - Loading Image Files!")
  folder_paths = ssc.get_folder_paths(batch_mode, input_folder, output_folder)
  # Sets the number of folders as a global variable, so it can be used in other update related functions.
  num_of_inputs = len(folder_paths)
  if (num_of_inputs == 0):
    print("Batch Mode Enabled, No Suitable Input Folders Found!")
    return 
  for path in folder_paths:
    images = ssc.load_images(path[0])
    if len(images) == 0 and num_of_inputs == 1:
      print("No Image Files Found!")
      return
    elif len(images) == 0:
      print(path[0] + " Has been skipped, No Image Files Found!")
      continue
    # The reason index is used here is because the core functions use intgers to switch between enforcement modes/types
    if width_enforce_type == 0:
      print("Working - Combining Image Files!")
    else:
      print("Working - Resizing & Combining Image Files!")
    resized_images = ssc.resize_images(images, width_enforce_type, custom_width)
    combined_image = ssc.combine_images(resized_images)
    print("Working - Slicing Combined Image into Finalized Images!")
    final_images = ssc.split_image(combined_image, split_height, senstivity, ignorable_pixels, scan_line_step)
    print("Working - Saving Finalized Images!")
    ssc.SaveData(final_images, path[1], output_files_type)
    print(path[1] + " Has Been Successfully Complete.")

# Example of a basic run => run_stitch_process("Chapter 1", split_height=5000, output_files_type=".png")
# You can add edit the other arguments to how you want them to be.
# Additional Arguments: batch_mode, width_enforce_type, custom_width, senstivity, ignorable_pixels, scan_line_step
# Take a look at the ReadMe for details on these arguments
run_stitch_process("Chapter 1", split_height=5000, output_files_type=".png")
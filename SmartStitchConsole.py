import SmartStitchCore as ssc
import argparse

def run_stitch_process(input_folder, split_height=5000, output_files_type=".png", batch_mode=False, width_enforce_type=0, custom_width=720, senstivity=90, ignorable_pixels=0, scan_line_step=5):
  """Runs the stitch process using the SS core functions, and updates the progress on the UI."""
  output_folder = input_folder + " [Stitched]"
  print("Process Starting Up")
  folder_paths = ssc.get_folder_paths(batch_mode, input_folder, output_folder)
  # Sets the number of folders as a global variable, so it can be used in other update related functions.
  num_of_inputs = len(folder_paths)
  if (num_of_inputs == 0):
    print("Batch Mode Enabled, No Suitable Input Folders Found!")
    return 
  for path in folder_paths:
    print("Working - Loading Image Files!")
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
    ssc.save_data(final_images, path[1], output_files_type)
    print(path[1] + " Has Been Successfully Complete.")
    print("Process Ended")

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--input_folder", "-i", type=str, required=True, help='Sets the path of Input Folder')
  parser.add_argument("--split_height", "-H", type=int, default=5000, help='Sets the value of the Rough Panel Height')
  parser.add_argument("--output_files_type", "-t", type=str, default=".png", choices=['.png', '.jpg', '.webp', '.bmp', '.tiff', '.tga'], help='Sets the type/format of the Output Image Files')
  parser.add_argument("--batch_mode", "-b", dest='batch_mode', action='store_true', help='Enables Batch Mode')
  parser.add_argument("--width_enforce_type", "-w", type=int, default=0, choices=[0, 1, 2], help='Selects the Ouput Image Width Enforcement Mode')
  parser.add_argument("--custom_width", "-cw", type=int, default=720, help='Selects the Custom Image Width For Width Enforcement Mode 2')
  parser.add_argument("--senstivity", "-s", type=int, default=90, choices=range(0,101), metavar="[0-100]", help='Sets the Object Detection Senstivity Percentage')
  parser.add_argument("--ignorable_pixels", "-ip", type=int, default=0, help='Sets the value of Ignorable Border Pixels')
  parser.add_argument("--scan_line_step", "-sl", type=int, default=5, choices=range(1,21), metavar="[1-20]", help='Sets the value of Scan Line Step')
  parser.set_defaults(batch_mode=False)

  args = parser.parse_args()
  run_stitch_process(args.input_folder, args.split_height, args.output_files_type, args.batch_mode, args.width_enforce_type, args.custom_width, args.senstivity, args.ignorable_pixels, args.scan_line_step)

if __name__ == '__main__':
  main()

# Example of a basic run => python SmartStitchConsole.py -i "Review me" -H 7500 -t ".png" -b
# This will Run the application on for input_folder of "./Review me" with split_height of 7500 and output_tyoe of ".png" and batch_mode enabled
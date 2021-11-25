<div align="center">
  <a href="https://github.com/MechTechnology/SmartStitch">
    <img alt="SmartStitch.Logo" width="200" heigth="200" src="https://github.com/MechTechnology/SmartStitch/blob/2fa9a190d94280003b3ac2f42fa9372025ccf3cb/SmartStitchLogo.png">
  </a>
  <h1>SmartStitch</h1>
  <p>
    A small yet powerful program for stitching and cutting webtoons/manhwa/manhua raws.
  </p>
  <p>
    GUI Version supports most versions of Windows, Console Version should work on any platform with Python Installed on it.
  </p>
  <a href="https://github.com/MechTechnology/SmartStitch/releases/latest">
    <img src="https://img.shields.io/github/release/MechTechnology/SmartStitch.svg?style=flat-square">
  </a>
  <a href="https://github.com/MechTechnology/SmartStitch/issues">
    <img src="https://img.shields.io/github/issues-raw/MechTechnology/SmartStitch.svg?style=flat-square">
  </a>
  <a href="https://github.com/MechTechnology/SmartStitch/issues">
    <img src="https://img.shields.io/github/issues-closed-raw/MechTechnology/SmartStitch.svg?style=flat-square">
  </a>
  <a href="https://github.com/MechTechnology/SmartStitch/issues">
    <img src="https://img.shields.io/github/issues-pr-raw/MechTechnology/SmartStitch.svg?style=flat-square">
  </a>
  <a href="https://github.com/MechTechnology/SmartStitch/issues">
    <img src="https://img.shields.io/github/issues-pr-closed-raw/MechTechnology/SmartStitch.svg?style=flat-square">
  </a>
</div>

## What is SmartStitch?
A small yet powerful program for stitching together webtoons/manhwa/manhua raws then slicing them down to the whatever size you wish for.

The smart part of the name comes from the fact that it uses some simple pixel calculation to stop itself from cutting/slicing through sfx or speech or drawings. it making life much easier for the team working on those raw images. [Both CLRD and TS will thank you a lot].

*It's not fancy, and does not use AI, but it's fast, robust, simple and more importantly works for me. (So i decided to share it with you!)*

## Screenshots
<div align="center">
<img alt="screenshot01" src="https://i.imgur.com/CEnMPvI.png">
<img alt="screenshot02" src="https://i.imgur.com/eLjHZXx.png">
</div>

## Quick Get Started GUI Version
1. Open the application.
2. Browse to your raw folder.
3. Set the Rough Panel Height of the output files.
4. Select a the output file type. (Supported types: png, jpg, webp, bmp, tiff, tga)
5. Click start process.
6. Done, Enjoy!

- Your file will be ordered the same way they are in your file explorer, so make sure everything is in order. (sort by name in file explorer)
- You can explore the advanced settings after reading documentation to have an better stitcher experience.

### How to launch the GUI Version (For Windows Users):
1. Download the program zip file of the latest release (Found in the releases section in this github)
2. Unzip the file to a suitable place on your device.
4. Put the raws you wish to stitch in a folder
5. Now the application will launch, and you can proceed with the Quick get started steps.

### How to launch the GUI Version (For Mac & Linux Users):
1. Do ```git clone https://github.com/AbhiMayadam/SmartStitch/```
2. Install python edition suitable for your machine. (Python 3.7 is recommended)
3. Open a terminal and send the following command: ```pip install numpy pillow natsort```
4. From the terminal, navigate to the directory where the source code was unzipped and send the following command: ```python3 SmartStitchGUI.py```
5. Now the application will launch, and you can proceed with the Quick get started steps.

## Reporting Bugs [2.0+]:
A logging system has been implemented in the GUI version of SmartStitch, when an error occur the application will inform you about it, and leaves the details in a file called 'crashreport.log', you can open an issue ticket here and attach the file, so it can be easily debugged and fixed.

And since it's just one person maintaining this application, only accepted tickets will be for version 2.0 and above. Please don't open tickets for lower versions, since your problem could have been already solved.

Please keep in mind that, if the issue is critical enough, it may require a copy of the raws files you used as input, but that will be for debugging special case issue, and will be requested if required.

You can also contact me at Discord if you don't want to use the GitHub Issue System. (MechTechnology#5466)


# Documentation
Here is the complete documentation for the application, it is broken down into 4 sections, basic settings, advanced settings, how to build your own version, how to run the console version.

## Basic Settings
These are the required settings that all users should be mindful of.

### Input Folder Path
Here you have to set the path for the Input Folder which contains the raws that will be processed by the program. If batch mode is enabled, it will search for subfolder within the given input path. So make sure your folder and files are in order.

*Console Parameter Name: --input_folder, -i*

### Rough Panel Height
Here you set the size that you want most panel to roughly be, the program will uses it as a guide to see where to slice/cut the images, however it IS ROUGH, meaning if the program finds bubbles/sfx/whatever at that specific pixel length, it will try to find the next closest position where it can cut the image. Thus the output size of each image will vary because of that, but they all will be roughly around this size.

*Default: 5000* --- *Console Parameter Name: --split_height, -H*

### Output type
The default output type is png since it is lossless, however you can always change to other types, such as jpg, the program does save jpg at 100 quality, so there should be not noticable loss in quality but it is up to the user what format they want.

*Default: .png* --- *Supported Types: png, jpg, webp, bmp, tiff, tga* --- *Console Parameter Name: --output_files_type, -t*

### Batch Mode
You can have multiple chapter folders in the input folder, when you turn on batch mode. The program will treat every folder within the input folder as its own chapter and will work on them. It will skip folders with no images, and if batch mode is enabled and no subfolders were found with the input folder/path, it will not run. It will show the associated message for each of those problems.

*Default: false* --- *Console Parameter Name: --batch_mode, -b*

## Advanced Settings
These are settings for more tech savvy people, or people that find themselves in a special case that need some fine tuning of the settings.

### Object Detection Senstivity (Percentage)
Before slicing at a specific height, the program checks the row of pixels it will slice at if there is bubbles/sfx/whatever, it compares neighbouring pixels for any drastic jump in value, (the allowed tolarence for jumps in pixel is the Object Detection Senstivity)

if there is too big of a jump in value between the pixels, that means there is something that shouldn't be cut, so it move up a pixel row and repeat. For 100 Senstivity will mean if entire pixel row does not have the same exact pixel value/color, it will not slice at it. For 0 Senstivity being it does not care about the pixel values and will cut there, essentially turning the program into a normal Dumb Image Slicer.

*Default: 90* --- *Value Range: 0-100* --- *Console Parameter Name: --senstivity, -s*

### Width Enforcement Mode and Custom Width [1.8+]
So essentially it's very straightforward. It adds a setting to select one of three modes to enforce change on the image width.
0 => No Enforcement, where you load the files as is, and work on them, if they vary in size, you will get some black lines in the side (Highest quality as there is no changes to the pixel values)
1 => Automatic uniform width, where you force all files to have the same width as the smallest file in the input folder.
2 => User Customized width, where the user specifies the width they want, that is the Custom Width parameter.
(Please just use waifu2x for upscaling raws, do not use this mode for it.)

*Default: 0* --- *Value Range: 0-2* --- *Console Parameter Name: --width_enforce_type, -w*
*Default: 720* --- *Console Parameter Name: --custom_width, -cw*

### Ignorable Border Pixels [2.0+]
This gives the option to ignore pixels on the border of the image when checking for bubbles/sfw/whatever. Why you might ask, Borders do not make the detection algorithm happy, so in some cases you want it to start its detection only inside said border, be careful to what value you want it to be since if it's larger that image it will case the program to crash/stop its operation.

*Default: 0* --- *Console Parameter Name: --ignorable_pixels, -ip*

### Scan Line Step [2.0+]
This is the step at which the program moves if it find the line it's on to be unsuitable to be sliced, meaning when it move on to the next line, it moves up/down X number of pixels to a new line, then it begins its scan algorithm once again. This X number of pixels is the scan line step. Smaller steps should give better results but larger ones do save computational power.

*Default: 5* --- *Value Range: 1-20* --- *Console Parameter Name: --scan_line_step, -sl*

#### Visualization of Ignorable Border Pixels and Scan Line Step
Red being the area ignored because of the Ignorable Border Pixels, and the blue lines would be the lines that application test for where it can slice (This example does not use the default values for those parameters)
<div align="center">
  <img alt="screenshot03" src="https://i.imgur.com/ipU6cJS.png">
</div>

### After Completion Subprocess [2.1+]
(GUI Only) With this option, one can set a specific console process to be fire on the output files of the application. For example, you can set it to fire waifu2x on the output files, so you can have the best raw processing experience. So how do we set that up,
  1. Enable the Show Advanced Settings
  2. Enable the Show Subprocess Settings
  3. Enable the run subprocess after completion flag.
  4. Set the process path/location, you can essentially browse to the process' exe file
  5. Set the arguments you want to pass to the process (Use the argument [stitched] to pass the output directory to your process).
  5. Optional: Use the argument [processed] to pass a custom output directory to your process for those that can't create their own output.

#### Visualization of After Completion Subprocess (Setup for waifu2x-caffe)
Of course you can use whatever version of waifu2x or process that you want, this is just an example of what i setup for myself.
<div align="center">
  <img alt="screenshot04" src="https://i.imgur.com/Vpl59rT.png">
</div>

## How to run the Console Version (For Windows, Mac, Linux Users)
1. Download the source code zip file of the latest release (Found in the releases section in this github)
2. Unzip the file to a suitable place on your device.
3. Install python edition suitable for your machine. (Python 3.7 is recommended)
4. Open a terminal and send the following command: pip install numpy pillow natsort
5. From the terminal, navigate to the directory where the source code was unzipped and run the command as per the usage details below

### Console Version Usage
```
python SmartStitchConsole.py [-h] -i INPUT_FOLDER
                                  [-H SPLIT_HEIGHT]
                                  [-t OUTPUT_FILES_TYPE]
                                  [-b]
                                  [-w {0,1,2}]
                                  [-cw CUSTOM_WIDTH]
                                  [-s [0-100]]
                                  [-ip IGNORABLE_PIXELS]
                                  [-sl [1-20]]
required arguments:
    --input_folder INPUT_FOLDER, -i INPUT_FOLDER               Sets the path of Input Folder
optional arguments:
  -h, --help                                                   Shows the help message and Exits
  --split_height SPLIT_HEIGHT, -H SPLIT_HEIGHT                 Sets the value of the Rough Panel Height
  --output_files_type OUTPUT_FILES_TYPE, -t OUTPUT_FILES_TYPE  Sets the type/format of the Output Image Files
  --batch_mode, -b                                             Enables Batch Mode
  --width_enforce_type {0,1,2}, -w {0,1,2}                     Selects the Ouput Image Width Enforcement Mode
  --custom_width CUSTOM_WIDTH, -cw CUSTOM_WIDTH                Selects the Custom Image Width For Width Enforcement Mode 2
  --senstivity [0-100], -s [0-100]                             Sets the Object Detection Senstivity Percentage
  --ignorable_pixels IGNORABLE_PIXELS, -ip IGNORABLE_PIXELS    Sets the value of Ignorable Border Pixels
  --scan_line_step [1-20], -sl [1-20]                          Scan Line Step
```

### Console Version Command Example
```
python SmartStitchConsole.py -i "Review me" -H 7500 -t ".png" -b
# This will Run the application on for input_folder of "./Review me" with split_height of 7500 and output_tyoe of ".png" and batch_mode enabled
```

## How to build/compile your own GUI Version?

### How to compile GUI package (For Windows Users)
1. Open a terminal and send the following command: ```pip install pyinstaller```
2. From the terminal, navigate to the directory where the source code was unzipped and run: ```pyinstaller SmartStitchGUI.spec```

### How to compile GUI package (For Mac users)
1. Install py2app using ```pip3 install py2app```
1a. Install numpy pillow natsort if you haven't with ```pip3 install numpy pillow natsort```
2. From the terminal, navigate to the directory where the source code was unzipped and run: ```python3 build.py py2app```
3. A folder will show up in the same directory called dist. Go in there and there will be SmartStitchGUI.app. You can run this by clicking on it.
4. You can drag this app to your Applications directory if you want.

- The output compiled application will not need python installed to run, but will only run on the platform it was built/compiled on.
- Mac and Linux Compiling was not tested by me, so uh... good luck xD
- P.S. macOS compilation does work using py2app, but cannot be shared for some reason or else it breaks - Abhi

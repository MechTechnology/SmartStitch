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
<img alt="screenshot01" src="https://i.imgur.com/iwiaDwD.png">
<img alt="screenshot02" src="https://i.imgur.com/nA1CZSL.png">
</div>

## Quick Get Started:
1. Download it from the release section in this github
2. Put the raws you wish to stitch in a folder
3. Open the application
4. Browse to your raw folder
5. Set the Rough Panel Height of the output files
7. Select a the output file type. (Supported types: png, jpg, webp, bmp, tiff, tga)
8. Click start process
9. Done, Enjoy

- Your file will be ordered the same way they are in your file explorer, so make sure everything is in order. (sort by name in file explorer)

## Reporting Bugs [2.0+]:
A logging system has been implemented in the GUI version of SmartStitch, when an error occur the application will inform you about it, and leaves the details in a file called 'crashreport.log', you can open an issue ticket here and attach the file, so it can be easily debugged and fixed. 

And since it's just one person maintaining this application, only accepted tickets will be for version 2.0 and above. Please don't open tickets for lower versions, since your problem could have been already solved.

You can also contact me at Discord if you don't want to use the GitHub Issue System. (MechTechnology#5466)

# Documentation
Here is the complete documentation for the application, it is broken down into 4 sections, basic settings, advanced settings, how to build your own version, how to run the console version.

## Basic Settings
These are the required settings that all users should be mindful of. 

### Rough Panel Height
Here you set the size that you want most panel to roughly be, the program will uses it as a guide to see where to slice/cut the images, however it IS ROUGH, meaning if the program finds bubbles/sfx/whatever at that specific pixel length, it will try to find the next closest position where it can cut the image. Thus the output size of each image will vary because of that, but they all will be roughly around this size.

*Default: 5000* --- *Console Parameter Name: split_height*

### Output type
The default output type is png since it is lossless, however you can always change to other types, such as jpg, the program does save jpg at 100 quality, so there should be not noticable loss in quality but it is up to the user what format they want.

*Default: .png* --- *Supported Types: png, jpg, webp, bmp, tiff, tga* --- *Console Parameter Name: output_files_type*

### Batch Mode
You can have multiple chapter folders in the input folder, when you turn on batch mode. The program will treat every folder within the input folder as its own chapter and will work on them. It will skip folders with no images, and if batch mode is enabled and no subfolders were found with the input folder/path, it will not run. It will show the associated message for each of those problems.

*Default: false* --- *Console Parameter Name: batch_mode*

## Advanced Settings
These are settings for more tech savvy people, or people that find themselves in a special case that need some fine tuning of the settings.

### Object Detection Senstivity (Percentage)
Before slicing at a specific height, the program checks the row of pixels it will slice at if there is bubbles/sfx/whatever, it compares neighbouring pixels for any drastic jump in value, (the allowed tolarence for jumps in pixel is the Object Detection Senstivity)

if there is too big of a jump in value between the pixels, that means there is something that shouldn't be cut, so it move up a pixel row and repeat. For 100 Senstivity will mean if entire pixel row does not have the same exact pixel value/color, it will not splice at it. For 0 Senstivity being it does not care about the pixel values and will cut there, essentially turning the program into a normal Dumb Image Slicer.

*Default: 90* --- *Value Range: 0-100* --- *Console Parameter Name: senstivity*

### Width Enforcement Mode and Custom Width [1.8+]
So essentially it's very straightforward. It adds a setting to select one of three modes to enforce change on the image width.
0 => No Enforcement, where you load the files as is, and work on them, if they vary in size, you will get some black lines in the side (Highest quality as there is no changes to the pixel values)
1 => Automatic uniform width, where you force all files to have the same width as the smallest file in the input folder.
2 => User Customized width, where the user specifies the width they want, that is the Custom Width parameter.
(Please just use waifu2x for upscaling raws, do not use)

*Default: 0* --- *Value Range: 0-2* --- *Console Parameter Name: width_enforce_type*
*Default: 720* --- *Console Parameter Name: custom_width*

### Ignorable Border Pixels [2.0+]
This is essentially the value of border pixels that you want the program to ignore when doing its object detection. Why you might ask, Borders do not make the detection algorithm happy, so in some cases you want it to start its detection only inside said border, be careful to what value you want it to be since if it's larger that image it will case the program to crash/stop its operation.

*Default: 0* --- *Console Parameter Name: ignorable_pixels*

### Scan Line Step [2.0+]
This is the step at which the program moves if it find the line it's on to be unsuitable to be sliced, meaning when it move on to the next line, it moves up/down X number of pixels to a new line, then it begins its scan algorithm once again. This X number of pixels is the scan line step. Smaller steps should give better results but larger ones do save computational power.

*Default: 5* --- *Value Range: 1-20* --- *Console Parameter Name: scan_line_step*

### Visualization of Ignorable Border Pixels and Scan Line Step
Red being the area ignored because of the Ignorable Border Pixels, and the blue lines would be the lines that application test for where it can slice (This example does not the default values for those parameters)
<div align="center">
  <img alt="screenshot01" src="https://i.imgur.com/ipU6cJS.png">
</div>

## Want to build your own GUI Verison?

### How to build GUI package --Windows
1. install PyInstaller if you haven't yet with the following command: pip install pyinstaller
2. then to create a build do: pyinstaller SmartStitchGUI.spec

### How to build a Single File GUI package --Windows
1. install PyInstaller if you haven't yet with the following command: pip install pyinstaller
2. then to create a build do: pyinstaller SmartStitchGUI_SingleFile.spec

## Want to run the Console Version?
Well you have to know python first of all, and then do the follow:
1. pip install all the needed packages in SmartStitchCore
2. open SmartStitchConsole, and call the stitch_process function and give it the required and optional parameters you desire.
refer to this documentation if you are confused on what each parameter does and what values it can take.


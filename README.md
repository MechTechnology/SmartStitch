# SmartStitch
A small program for stitching together webtoons/manhwa/manhua raws.
It's not fancy, and does not use AI, but it's fast, simple and more importantly works for me. (So i decided to share it with you!)

### How to Use:
1. Download it from the release section in this github
2. Put the raws you wish to stitch in a folder
3. Open the application
4. Browse to your raw folder
5. Set the rough height/length of the output files
6. Set the sentivity or leave it as is (setting it as 0, would turn off the smart aspect and you will get a normal image combiner)
7. Click start process
8. Done, Enjoy

- Number your files correctly and don't use single digit numbering since it might mix up your files
- Bad: 1,2,3...10,11,12), Good: 01,02,03,...10,11,12

### How it Works (and What is Sentivity)
- how it works is that it combines everything into a single image, and then starts slicing it into smaller ones
- Before slicing thou, it checks the row of pixels it will slice at if there is bubbles or whatever, it compares neighbouring pixels for any drastic jump in value, (tolarence for value jumps is the sentivity)
- if there is too big of a jump in value between the pixels, that means there is something that shouldn't be cut, so it move up a pixel row and repeat.
- For senstivity 100 will mean if the pixel row that it will slice at will have to be the same color, 0 being it does not care so it will cut there

### How to built --Windows
1. install PyInstaller if you haven't yet with the following command: pip install pyinstaller
3. then to create a build do: pyinstaller SmartStitchGUI.spec

### How single file --Windows
1. install PyInstaller if you haven't yet with the following command: pip install pyinstaller
3. then to create a build do: pyinstaller singleFile.spec
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from PIL import Image as pil
from natsort import natsorted
import numpy as np
import os
import time
import pickle
import threading

class SmartStitch(Tk):
    def __init__(self, *args, **kwargs):
        # Initalizes a tk window with the give parameters of the constructor.
        Tk.__init__(self, *args, **kwargs)

        # Global Variables
        self.input_folder = StringVar()
        self.output_folder = StringVar()
        self.batch_mode = IntVar()
        self.split_height = StringVar(value="5000")
        self.senstivity = StringVar(value="90")
        self.status = StringVar(value="Idle")
        self.output_type = StringVar(value=".jpg")
        self.width_enforce_type = StringVar(value="No Width Enforcement")
        self.custom_width = StringVar(value="720")
        self.num_of_inputs = 1
        self.progress = ""
        self.actionbutton = ""
        self.widthfieldtitle = ""
        self.widthfield = ""
        self.widthdisclamer = ""

        # Componant Setup
        self.SetupWindow()
        self.SetupBrowseFrame().grid(row=0, column=0, padx=(15), pady=(15), sticky="new")
        self.SetupSettingsFrame().grid(row=1, column=0, padx=(15), pady=(0,15), sticky="new")
        self.SetupStatusFrame().grid(row=2, column=0, padx=(15), pady=(0,15), sticky="new")
        self.SetupActionFrame().grid(row=3, column=0, padx=(15), pady=(0,15), sticky="new")
        self.LoadPrevSettings()
        self.UpdateWidthMode()

    def geticon(self, relative_path):    
        if not hasattr(sys, "frozen"):
            relative_path = os.path.join(os.path.dirname(__file__), relative_path)
        else:
            relative_path = os.path.join(sys.prefix, relative_path)
        return relative_path

        # return os.path.join(base_path, relative_path)
    def SetupWindow(self):
        # Sets up Title and Logo
        self.title('SmartStitch by MechTechnology [1.9]')
        self.iconbitmap(default=self.geticon("SmartStitchLogo.ico"))

        # Sets Window Size, centers it on Launch and Prevents Resize.
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (self.winfo_screenwidth()/2) - (window_height/2) - 220
        y = (self.winfo_screenheight()/2) - (window_width/2) - 200
        self.geometry('+%d+%d' % (x, y))
        self.columnconfigure(0, weight=1)
        self.resizable(False, False)

    def LoadPrevSettings(self):
        # loads the setting on start up (creates if it does not exist)
        settings_pickle = "settings.pickle"
        if not os.path.exists(settings_pickle):
            self.SaveCurrentSettings()
        else:
            with open(settings_pickle, "rb") as settings_handle:
                settings = pickle.load(settings_handle)
                self.split_height.set(settings[0])
                self.senstivity.set(settings[1])
                self.output_type.set(settings[2])
                self.width_enforce_type.set(settings[3])
                self.custom_width.set(settings[4])

    def SaveCurrentSettings(self, *args):
        # Saves the settings
        settings = []
        settings.append(self.split_height.get())
        settings.append(self.senstivity.get())
        settings.append(self.output_type.get())
        settings.append(self.width_enforce_type.get())
        settings.append(self.custom_width.get())

        settings_pickle = "settings.pickle"
        with open(settings_pickle, 'wb') as settings_handle:
            pickle.dump(settings, settings_handle)  

    def SetupBrowseFrame(self):
        # Browse Button and Input and Output Field
        browse_frame = Frame(self)
        browse_label = ttk.Label(browse_frame, text = 'Input Path')
        browse_field = ttk.Entry(browse_frame, textvariable=self.input_folder)
        browse_field.bind("<Any-KeyRelease>", self.UpdateOutputFolder)
        browse_button = ttk.Button(browse_frame, text = 'Browse', command=self.BrowseToCommand)
        output_label = ttk.Label(browse_frame, text = 'Output Path')
        output_field = ttk.Entry(browse_frame, textvariable=self.output_folder)
        batch_checkbox = ttk.Checkbutton(browse_frame, variable=self.batch_mode, text = 'Batch Mode [Input folder contains multiple chapter folders]')
        browse_label.grid(row = 0,column = 0, sticky="new")
        browse_field.grid(row = 1, column = 0, pady=(2,0), sticky="new")
        browse_button.grid(row = 1,column = 1, padx=(15, 0), sticky="ne")
        output_label.grid(row = 2, column = 0, sticky="new")
        output_field.grid(row = 3, column = 0, columnspan=2, pady=(2,0), sticky="new")
        batch_checkbox.grid(row = 4, column = 0, columnspan=2, pady=(2,0), sticky="new")
        browse_frame.columnconfigure(0, weight=1)
        return browse_frame

    def BrowseToCommand(self):
        # Allow user to select a directory and updates input_folder and output_folder
        foldername = filedialog.askdirectory()
        self.input_folder.set(foldername)
        self.output_folder.set(foldername + " [Stitched]")

    def UpdateOutputFolder(self, *args):
        foldername = self.input_folder.get()
        self.output_folder.set(foldername + " [Stitched]")

    def SetupSettingsFrame(self):
        # Browse Split Field and Senstivity Fields
        settings_frame = Frame(self)
        split_label = ttk.Label(settings_frame, text = 'Rough Panel Height (In Pixels):')
        split_field = ttk.Entry(settings_frame, textvariable=self.split_height, validate='all')
        split_field.bind("<Any-KeyRelease>", self.SaveCurrentSettings)
        split_field['validatecommand'] = (split_field.register(self.AllowNumOnly),'%P','%d','%s')
        senstivity_label = ttk.Label(settings_frame, text = 'Bubble Detection Senstivity (0-100%):')
        senstivity_field = ttk.Entry(settings_frame, textvariable=self.senstivity, validate='all')
        senstivity_field.bind("<Any-KeyRelease>", self.SaveCurrentSettings)
        senstivity_field['validatecommand'] = (senstivity_field.register(self.AllowPercentOnly),'%P','%d','%s')
        type_label = ttk.Label(settings_frame, text = 'Output Images Type:')
        type_dropdown = ttk.Combobox(settings_frame, textvariable=self.output_type, values=('.jpg', '.png', '.webp', '.bmp', '.tiff', '.tga'))
        type_dropdown.bind("<<ComboboxSelected>>", self.SaveCurrentSettings)
        width_enforce_label = ttk.Label(settings_frame, text = 'Output Width Enforcement:')
        width_enforce_dropdown = ttk.Combobox(settings_frame, textvariable=self.width_enforce_type, values=('No Width Enforcement', 'Automatic Uniform Width', 'User Customized Width'))
        width_enforce_dropdown.bind("<<ComboboxSelected>>", self.UpdateWidthMode)
        self.widthfieldtitle = ttk.Label(settings_frame, text = 'Custom Width to be Enforced (In Pixels):')
        self.widthfield = ttk.Entry(settings_frame, textvariable=self.custom_width, validate='all')
        self.widthfield.bind("<Any-KeyRelease>", self.SaveCurrentSettings)
        self.widthfield['validatecommand'] = (split_field.register(self.AllowNumOnly),'%P','%d','%s')
        self.widthdisclamer = ttk.Label(settings_frame, foreground='red', text = 'Disclaimer:', justify=LEFT, wraplength=380)
        split_label.grid(row=0, column=0, sticky="new")
        split_field.grid(row=1, column=0, pady=(2,0), sticky="new")
        senstivity_label.grid(row = 0, column = 1, padx=(15, 0), sticky="new")
        senstivity_field.grid(row = 1, column = 1, padx=(15, 0), pady=(2,0), sticky="new")
        type_label.grid(row = 2, column = 0, pady=(5,0), sticky="new")
        type_dropdown.grid(row = 3, column = 0, pady=(2,0), sticky="new")
        width_enforce_label.grid(row = 2, column = 1, padx=(15, 0), pady=(5,0), sticky="new")
        width_enforce_dropdown.grid(row = 3, column = 1, padx=(15, 0), pady=(2,0), sticky="new")
        settings_frame.columnconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=1)
        return settings_frame
    
    def AllowNumOnly(self,P,d,s):
        #If the Keyboard is trying to insert value
        if d == '1': 
            if not (P.isdigit()):
                return False
        return True
    
    def AllowPercentOnly(self,P,d,s):
        #If the Keyboard is trying to insert value
        if d == '1': 
            if not (P.isdigit() and len(s) < 3 and int(P)<=100):
                return False
        return True

    def UpdateWidthMode(self, *args):
        enforce_type = self.width_enforce_type.get()
        if enforce_type == 'Automatic Uniform Width':
            self.widthfieldtitle.grid_remove()
            self.widthfield.grid_remove()
            self.widthdisclamer['text'] = 'Disclaimer: This width enforcement mode will cause files with a larger width to be resized down (using LANCZOS) to the width of smallest input file.'
            self.widthdisclamer.grid(row = 6, column = 0, columnspan=2, pady=(5,0), sticky="new")
        elif enforce_type == 'User Customized Width':
            self.widthfieldtitle.grid(row = 4, column = 0, columnspan=2, pady=(5,0), sticky="new")
            self.widthfield.grid(row = 5, column = 0, columnspan=2, pady=(2,0), sticky="new")
            self.widthdisclamer['text'] = 'Disclaimer: This width enforcement mode will cause all files to be resized (using LANCZOS) to the width you specify. Please use tools like waifu2x for large upscaling.'
            self.widthdisclamer.grid(row = 6, column = 0, columnspan=2, pady=(5,0), sticky="new")
        else:
            self.widthfieldtitle.grid_remove()
            self.widthfield.grid_remove()
            self.widthdisclamer.grid_remove()
        if args != ():
            self.SaveCurrentSettings()        
    
    def SetupStatusFrame(self):
        status_frame = Frame(self)
        status_label = ttk.Label(status_frame, text = 'Status:')
        status_field = ttk.Entry(status_frame, textvariable=self.status)
        status_field.config(state=DISABLED)
        status_label.grid(row = 0,column = 0, sticky="new")
        status_field.grid(row = 1, column = 0, pady=(2,0), sticky="new")
        status_frame.columnconfigure(0, weight=1)
        return status_frame

    def SetupActionFrame(self):
        action_frame = Frame(self)
        self.progress = ttk.Progressbar(action_frame)
        self.actionbutton = ttk.Button(action_frame, text = 'Start Process', command=self.RunStitchProcessAsync)
        self.progress.grid(row = 0, column = 0, columnspan = 2, pady=(2,0), sticky="new")
        self.actionbutton.grid(row = 0, column = 2, padx=(15, 0), sticky="new")
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)
        action_frame.columnconfigure(2, weight=1)
        return action_frame

    def SetBatchFolders(self):
        batch_input_folder = self.input_folder.get()
        batch_output_folder = self.output_folder.get()
        input_folders = [os.path.abspath(os.path.join(batch_input_folder, name)) for name in os.listdir(batch_input_folder) if os.path.isdir(os.path.join(batch_input_folder, name))]
        output_folders = [os.path.abspath(os.path.join(batch_output_folder, name + " [Stitched]" )) for name in os.listdir(batch_input_folder) if os.path.isdir(os.path.join(batch_input_folder, name))]
        return input_folders, output_folders

    def LoadImages(self, foldername):
        # Loads all image files in a given folder into a list of pillow image objects
        images = []
        if (foldername == ""):
            return images
        folder = os.path.abspath(str(foldername))
        files = natsorted(os.listdir(folder))
        if len(files) == 0:
            return images
        for imgFile in files:
            if imgFile.endswith(('.png', '.webp', '.jpg', '.jpeg', '.jfif', '.bmp', '.tiff', '.tga')):
                imgPath = os.path.join(folder, imgFile)
                image = pil.open(imgPath)
                images.append(image)
        return images

    def ResizeImages(self, images):
        #Resizes the images according to what enforcement mode you have.
        enforce_type = self.width_enforce_type.get()
        if enforce_type == "No Width Enforcement":
            return images
        else:
            resized_images = []
            new_image_width = 0
            if enforce_type == 'Automatic Uniform Width':
                widths, heights = zip(*(image.size for image in images))
                new_image_width = min(widths)
            elif enforce_type == 'User Customized Width':
                new_image_width = int(self.custom_width.get())
            for image in images:
                if image.size[0] == new_image_width:
                    resized_images.append(image)
                else:
                    ratio = float(image.size[1] / image.size[0])
                    new_image_height = int(ratio * new_image_width)
                    new_image = image.resize((new_image_width, new_image_height), pil.ANTIALIAS)
                    resized_images.append(new_image)
            return resized_images

    def CombineVertically(self, images):
        # All this does is combine all the files into a single image in the memory.
        widths, heights = zip(*(image.size for image in images))
        new_image_width = max(widths)
        new_image_height = sum(heights)
        new_image = pil.new('RGB', (new_image_width, new_image_height))
        combine_offset = 0
        for image in images:
            new_image.paste(image, (0, combine_offset))
            combine_offset += image.size[1]
        return new_image

    def SmartAdjust(self, combined_pixels, split_height, split_offset, senstivity):
        # Where the smart magic happens, compares pixels of each row, to decide if it's okay to cut there
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
            prev_pixel = int(pixel_row[0])
            for x in range(1, len(pixel_row)-1):
                current_pixel = int(pixel_row[x])
                pixel_value_diff = current_pixel - prev_pixel
                if (pixel_value_diff < -threshold or pixel_value_diff > threshold):
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

    def SplitVertical(self, combined_img):
        # Splits the gaint combined img into small images passed on desired height.
        split_height = int(self.split_height.get())
        senstivity = int(self.senstivity.get())
        max_width = combined_img.size[0]
        max_height = combined_img.size[1]
        combined_pixels = np.array(combined_img.convert('L'))
        images = []

        # The spliting starts here (calls another function to decide where to slice)
        split_offset = 0
        while((split_offset + split_height) < max_height):
            new_split_height = self.SmartAdjust(combined_pixels, split_height, split_offset, senstivity)
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

    def SaveData(self, data, foldername):
        # Saves the given images/date in the output folder!
        new_folder = str(foldername)
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        imageIndex = 1
        outputformat = self.output_type.get()
        progress_value = self.progress['value']
        for image in data:
            image.save(new_folder + '/' + str(f'{imageIndex:02}') + outputformat, quality=100)
            imageIndex += 1
            progress_value += ((60 * 1/len(data)) / self.num_of_inputs)
            self.progress['value'] = progress_value
            Tk.update_idletasks(self)
        return

    def RunStitchProcess(self):
        # Fires the process sequence from the GUI
        self.actionbutton['state'] = "disabled"
        self.actionbutton.update()
        if(self.split_height.get() == "" or self.split_height.get() =="0"):
            self.status.set("Idle - Split height value was not set!")
            self.actionbutton['state'] = "normal"
            return
        if(self.senstivity.get() == "" or self.senstivity.get() == "0"):
            self.status.set("Idle - Senstivity value was not set!")
            self.actionbutton['state'] = "normal"
            return
        start = time.time()
        self.status.set("Working - Loading Image Files!")
        self.progress['value'] = 0
        Tk.update_idletasks(self)
        input_folders = []
        output_folders = []
        if self.batch_mode.get() == 0:
            input_folders.append(self.input_folder.get())
            output_folders.append(self.output_folder.get())
        else:
            input_folders , output_folders = self.SetBatchFolders()
        self.num_of_inputs = len(input_folders)
        for folder in input_folders:
            images = self.LoadImages(folder)
            if len(images) == 0:
                self.status.set("Idle - No Image Files Found!")
                self.actionbutton['state'] = "normal"
                return
            if self.width_enforce_type.get() == "No Width Enforcement":
                self.status.set("Working - Combining Image Files!")
            else:
                self.status.set("Working - Resizing & Combining Image Files!")
            self.progress['value'] += (10 / self.num_of_inputs)
            Tk.update_idletasks(self)
            resized_images = self.ResizeImages(images)
            combined_image = self.CombineVertically(resized_images)
            self.status.set("Working - Slicing Combined Image into Finalized Images!")
            self.progress['value'] += (10 / self.num_of_inputs)
            Tk.update_idletasks(self)
            final_images = self.SplitVertical(combined_image)
            self.status.set("Working - Saving Finalized Images!")
            self.progress['value'] += (20 / self.num_of_inputs)
            Tk.update_idletasks(self)
            outfolder = output_folders[input_folders.index(folder)]
            self.SaveData(final_images, outfolder)
        end = time.time()
        delta = end - start
        self.status.set("Idle - Files successfully stitched in " +  str(delta) + "sec!")
        self.progress['value'] = 100
        self.actionbutton['state'] = "normal"
    
    def RunStitchProcessAsync(self):
        workthread = threading.Thread(target=self.RunStitchProcess)
        workthread.start()
    

SmartStitch().mainloop()
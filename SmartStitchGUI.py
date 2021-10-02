from tkinter import *
from tkinter import ttk, filedialog
from datetime import datetime
from time import time
import os
import pickle
import logging
import threading
import SmartStitchCore as ssc

class SmartStitchGUI(Tk):
  def __init__(self):
    """GUI Default Constructor."""
    # Intializes Tkinter Window.
    super().__init__()
    # Application Basic Settings Variables
    self.input_folder = StringVar()
    self.output_folder = StringVar()
    self.enable_batch_mode = BooleanVar()
    self.split_height = StringVar(value="5000")
    self.output_files_type = StringVar(value=".png")
    # Application Advance Settings Variables
    self.show_advanced_settings = BooleanVar(False)
    self.slicing_senstivity = StringVar(value="90")
    self.ignorable_edges_pixels = StringVar(value="0")
    self.scan_line_step = StringVar(value="5")
    self.width_enforce_type = StringVar(value="No Width Enforcement")
    self.custom_enforce_width = StringVar(value="720")
    self.show_subprocess_settings = BooleanVar(False)
    self.enable_subprocess_execution = BooleanVar(False)
    self.subprocess_path = StringVar()
    self.subprocess_arguments = StringVar()
    # GUI related Variables
    self.status = StringVar(value="Idle")
    self.num_of_inputs = 1
    self.progress = ""
    self.progress = ""
    self.subprocess_console = ""
    self.width_enforce_types = ['No Width Enforcement', 'Automatic Uniform Width', 'User Customized Width']
    # Application StartUp Sequence
    self.load_app_settings()
    self.setup_window(app_maintainer="MechTechnology", app_version="2.1.2")
    self.setup_paths_frame().grid(row=0, column=0, padx=(10), sticky="new")
    self.setup_basic_settings_frame().grid(row=1, column=0, padx=(10), pady=(5,0), sticky="new")
    self.setup_advanced_settings_frame().grid(row=2, column=0, padx=(10), pady=(5,0), sticky="new")
    self.setup_action_frame().grid(row=4, column=0, padx=(10), pady=(5), columnspan=2, sticky="new")

  def save_app_settings(self, *args):
    """Saves active application settings in a Pickle file."""
    app_settings = []
    app_settings.append(self.enable_batch_mode.get())
    app_settings.append(self.split_height.get())
    app_settings.append(self.output_files_type.get())
    app_settings.append(self.show_advanced_settings.get())
    app_settings.append(self.slicing_senstivity.get())
    app_settings.append(self.ignorable_edges_pixels.get())
    app_settings.append(self.width_enforce_type.get())
    app_settings.append(self.custom_enforce_width.get())
    app_settings.append(self.show_subprocess_settings.get())
    app_settings.append(self.enable_subprocess_execution.get())
    app_settings.append(self.subprocess_path.get())
    app_settings.append(self.subprocess_arguments.get())
    with open("settings.pickle", "wb") as app_settings_handler:
      pickle.dump(app_settings, app_settings_handler)

  def load_app_settings(self):
    """Loads application settings from a Pickle file."""
    if not os.path.exists("settings.pickle"):
      self.save_app_settings()
    else:
      with open("settings.pickle", 'rb') as app_settings_handler:
        saved_settings = pickle.load(app_settings_handler)
        self.enable_batch_mode.set(saved_settings[0])
        self.split_height.set(saved_settings[1])
        self.output_files_type.set(saved_settings[2])
        self.show_advanced_settings.set(saved_settings[3])
        self.slicing_senstivity.set(saved_settings[4])
        self.ignorable_edges_pixels.set(saved_settings[5])
        self.width_enforce_type.set(saved_settings[6])
        self.custom_enforce_width.set(saved_settings[7])
        self.show_subprocess_settings.set(saved_settings[8])
        self.enable_subprocess_execution.set(saved_settings[9])
        self.subprocess_path.set(saved_settings[10])
        self.subprocess_arguments.set(saved_settings[11])
    
  def setup_window(self, app_maintainer, app_version):
    """Sets up Basic Attributes about the window such Application Logging, Title, Icon and Position on Start Up."""
    # Sets up Title and Logo
    self.title("SmartStitch by " + app_maintainer + " [" + app_version + "]")
    icon_abs_path = os.path.join(os.path.dirname(__file__), "SmartStitchLogo.ico")
    self.iconbitmap(icon_abs_path)
    # Configures logging to save into a log file.
    logging.basicConfig(filename="crashreport.log", level=logging.WARNING)
    # Centers the window on Launch and Disables Resize.
    window_width = self.winfo_width()
    window_height = self.winfo_height()
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()
    x = (self.winfo_screenwidth()/2) - (window_height/2) - 120
    y = (self.winfo_screenheight()/2) - (window_width/2) - 120
    self.geometry('+%d+%d' % (x, y))
    self.columnconfigure(0, weight=1)
    self.resizable(False, False)

  def setup_paths_frame(self):
    """Setups the Fields for the Input and Output Paths."""
    # Browse Button and Input and Output Field
    paths_frame = LabelFrame(self, text="Input/Output Settings", padx=(5))
    paths_frame.columnconfigure(0, weight=1)
    # Setup of Input Label, Entry Field, and Browse Button.
    input_label = ttk.Label(paths_frame, text = 'Input Path')
    input_field = ttk.Entry(paths_frame, textvariable=self.input_folder)
    input_field.bind("<Any-KeyRelease>", self.update_output_path)
    input_button = ttk.Button(paths_frame, text = 'Browse', command=self.browse_input_path)
    input_label.grid(row = 0,column = 0, sticky="new")
    input_field.grid(row = 1, column = 0, pady=(2,0), sticky="new")
    input_button.grid(row = 1,column = 1, padx=(15, 0), sticky="ne")
    # Setup of Output Label and Entry Field.
    output_label = ttk.Label(paths_frame, text = 'Output Path')
    output_field = ttk.Entry(paths_frame, textvariable=self.output_folder)
    output_label.grid(row = 2, column = 0, sticky="new")
    output_field.grid(row = 3, column = 0, columnspan=2, pady=(2,0), sticky="new")
    # Setup of Back Mode Selector/Checkbox.
    batch_checkbox = ttk.Checkbutton(paths_frame, variable=self.enable_batch_mode, text = 'Batch Mode [Input folder contains multiple chapter folders]', command=self.save_app_settings)
    batch_checkbox.grid(row = 4, column = 0, columnspan=2, pady=(2,5), sticky="new")
    return paths_frame

  def setup_basic_settings_frame(self):
    """Setups the basic settings controls that most user would need."""
    basic_settings_frame = LabelFrame(self, text="Basic Settings", padx=(5))
    basic_settings_frame.columnconfigure(0, weight=1, uniform="equal")
    basic_settings_frame.columnconfigure(1, weight=1, uniform="equal")
    # Setup of Split Height Label, Entry Field, and Browse Button.
    split_label = ttk.Label(basic_settings_frame, text = 'Rough Panel Height (In Pixels):        ')
    split_field = ttk.Entry(basic_settings_frame, textvariable=self.split_height, validate='all')
    split_field.bind("<Any-KeyRelease>", self.save_app_settings)
    split_field['validatecommand'] = (split_field.register(self.validate_nums_only),'%P','%d','%s')
    split_label.grid(row=0, column=0, padx=(0,5), sticky="new")
    split_field.grid(row=1, column=0, padx=(0,5), pady=(2,0), sticky="new")
    # Setup of Output File Type Settings' Label, and Entry Field.
    type_label = ttk.Label(basic_settings_frame, text = 'Output Images Type:')
    type_dropdown = ttk.Combobox(basic_settings_frame, textvariable=self.output_files_type, values=('.png', '.jpg', '.webp', '.bmp', '.tiff', '.tga'))
    type_dropdown.bind("<<ComboboxSelected>>", self.save_app_settings)
    type_label.grid(row = 0, column = 1, padx=(5,0), sticky="new")
    type_dropdown.grid(row = 1, column = 1,  padx=(5, 0), pady=(2,10), sticky="new")
    return basic_settings_frame

  def setup_advanced_settings_frame(self):
    """Setups the basic settings controls that most user would need."""
    # Setup of Main Wrapper Frame That holds the advanced settings and its toggle checkbox
    advanced_settings_frame = Frame(self)
    advanced_settings_frame.columnconfigure(0, weight=1)
    # Setup of a Frame That holds the settings is toggleable by a checkbox
    shown_settings_frame = LabelFrame(advanced_settings_frame, text="Advanced Settings", padx=(5))
    shown_settings_frame.columnconfigure(0, weight=1, uniform="equal")
    shown_settings_frame.columnconfigure(1, weight=1, uniform="equal")
    # Setup of Slice Senstivity Settings' Label, and Entry Field.
    senstivity_label = ttk.Label(shown_settings_frame, text = 'Object Detection Sensitivity (%):')
    senstivity_field = ttk.Entry(shown_settings_frame, textvariable=self.slicing_senstivity, validate='all')
    senstivity_field.bind("<Any-KeyRelease>", self.save_app_settings)
    senstivity_field['validatecommand'] = (senstivity_field.register(self.validate_percentage_only),'%P','%d','%s')
    senstivity_label.grid(row = 0, column = 0, padx=(0,5), sticky="new")
    senstivity_field.grid(row = 1, column = 0, padx=(0,5), pady=(2,5), sticky="new")
    # Setup of Ignorable Pixels Senstivity Settings' Label, and Entry Field.
    ignorable_pixels_label = ttk.Label(shown_settings_frame, text = 'Ignorable Border Pixels:')
    ignorable_pixels_field = ttk.Entry(shown_settings_frame, textvariable=self.ignorable_edges_pixels, validate='all')
    ignorable_pixels_field.bind("<Any-KeyRelease>", self.save_app_settings)
    ignorable_pixels_field['validatecommand'] = (ignorable_pixels_field.register(self.validate_nums_only),'%P','%d','%s')
    ignorable_pixels_label.grid(row = 0, column = 1, padx=(5, 0), sticky="new")
    ignorable_pixels_field.grid(row = 1, column = 1, padx=(5, 0), pady=(2,5), sticky="new")
    # Setup of Scan Line Step Settings' Label, and Entry Field.
    scan_line_label = ttk.Label(shown_settings_frame, text = 'Scan Line Step:')
    scan_line_field = ttk.Entry(shown_settings_frame, textvariable=self.scan_line_step, validate='all')
    scan_line_field.bind("<Any-KeyRelease>", self.save_app_settings)
    scan_line_field['validatecommand'] = (scan_line_field.register(self.validate_onetotwenty_only),'%P','%d','%s')
    scan_line_label.grid(row = 2, column = 0, padx=(0,5), sticky="new")
    scan_line_field.grid(row = 3, column = 0, padx=(0,5), pady=(2,5), sticky="new")
    # Set of Custom Width Enforcement Settings' Label and Entry Field and Width
    widthfieldtitle = ttk.Label(shown_settings_frame, text = 'Custom Width to be Enforced (In Pixels):')
    widthfield = ttk.Entry(shown_settings_frame, textvariable=self.custom_enforce_width, validate='all')
    widthfield.bind("<Any-KeyRelease>", self.save_app_settings)
    widthfield['validatecommand'] = (widthfield.register(self.validate_nums_only),'%P','%d','%s')
    # Setup of Width Enforcement Settings' Label, and Entry Field.
    width_enforce_label = ttk.Label(shown_settings_frame, text = 'Output Width Enforcement:')
    width_enforce_dropdown = ttk.Combobox(shown_settings_frame, textvariable=self.width_enforce_type, values=('No Width Enforcement', 'Automatic Uniform Width', 'User Customized Width'))
    width_enforce_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_width_mode(widthfieldtitle, widthfield))
    width_enforce_label.grid(row = 2, column = 1, padx=(5, 0), sticky="new")
    width_enforce_dropdown.grid(row = 3, column = 1, padx=(5, 0), pady=(2,5), sticky="new")
    # Setup of Toggle Button to show subprocess settings or not.
    subprocess_setting_frame = self.setup_subprocess_frame()
    show_subprocess_checkbox = ttk.Checkbutton(shown_settings_frame, variable=self.show_subprocess_settings, text = 'Show Subprocess Settings [For Experienced Users Only]', command=lambda: self.subprocess_setting_toggle(subprocess_setting_frame))
    show_subprocess_checkbox.grid(row = 6, column = 0, columnspan=2,pady=(5), sticky="new") 
    # Setup of Toggle Button to show advanced settings or not.
    show_advanced_checkbox = ttk.Checkbutton(advanced_settings_frame, variable=self.show_advanced_settings, text = 'Show Advanced Settings', command=lambda: self.advanced_settings_toggle(shown_settings_frame, subprocess_setting_frame))
    show_advanced_checkbox.grid(row = 0, column = 0, columnspan=2, pady=(2,5), sticky="new")
    # On first setup decides to display or the needed elements.
    self.advanced_settings_toggle(shown_settings_frame, subprocess_setting_frame)
    self.update_width_mode(widthfieldtitle, widthfield)
    return advanced_settings_frame

  def setup_subprocess_frame(self):
    """Setups the Fields for the Subprocess Parameters."""
    # Browse Button and Input and Output Field
    subprocess_frame = LabelFrame(self, text="Subprocess Settings", padx=(5))
    subprocess_frame.columnconfigure(0, weight=1)
    # Setup of Toggle Button to enable subprocess execution settings or not.
    show_advanced_checkbox = ttk.Checkbutton(subprocess_frame, variable=self.enable_subprocess_execution, text = 'Run the following subprocess after stitching is complete', command=lambda: self.save_app_settings)
    show_advanced_checkbox.grid(row = 0, column = 0, columnspan=2, pady=(2,5), sticky="new")
    # Setup of Path Label, Entry Field, and Browse Button.
    subprocess_path_label = ttk.Label(subprocess_frame, text = 'Subprocess File Location/Path')
    subprocess_path_field = ttk.Entry(subprocess_frame, textvariable=self.subprocess_path)
    subprocess_path_button = ttk.Button(subprocess_frame, text = 'Browse', command=self.browse_subprocess_path)
    subprocess_path_field.bind("<Any-KeyRelease>", self.update_subprocess_path)
    subprocess_path_label.grid(row = 1,column = 0, sticky="new")
    subprocess_path_field.grid(row = 2, column = 0, pady=(2,0), sticky="new")
    subprocess_path_button.grid(row = 2,column = 1, padx=(15, 0), sticky="ne")
    # Setup of Arguments Label and Entry Field.
    subprocess_arguments_label = ttk.Label(subprocess_frame, text = 'Subprocess Arguments')
    subprocess_arguments_field = ttk.Entry(subprocess_frame, textvariable=self.subprocess_arguments)
    subprocess_arguments_field.bind("<Any-KeyRelease>", self.save_app_settings)
    subprocess_arguments_label.grid(row = 3, column = 0, sticky="new")
    subprocess_arguments_field.grid(row = 4, column = 0, columnspan=2, pady=(2,0), sticky="new")
    # Setup of Back Mode Selector/Checkbox.
    argument_hint_label = ttk.Label(subprocess_frame, foreground='blue', text = 'To pass the stitch output directory use the argument [stitched], to pass a custom process output directory use the argument [processed]', justify=LEFT, wraplength=380)
    argument_hint_label.grid(row=5, column=0, columnspan=2, pady=(2,0), sticky="new")
    output_label = ttk.Label(subprocess_frame, text = 'Subprocess Console Output')
    # Setup of the Subprocess Console.
    output_label.grid(row=6, column=0, columnspan=2, pady=(5,0), sticky="new")
    self.subprocess_console = Label(subprocess_frame, foreground="white",background="#333", height=12, anchor="sw", justify=LEFT)
    self.subprocess_console.grid(row=7, column=0, columnspan=2, pady=(0,5), sticky="news")
    # Inserting Text which is read only
    return subprocess_frame

  def setup_action_frame(self):
    action_frame = LabelFrame(self, padx=(5))
    status_label = ttk.Label(action_frame, text='Current Status:')
    status_field = ttk.Entry(action_frame, textvariable=self.status)
    status_field.config(state=DISABLED)
    status_label.grid(row = 0, column=0, columnspan=3, sticky="new")
    status_field.grid(row = 1, column=0, columnspan=3, pady=(2,5), sticky="new")
    self.progress = ttk.Progressbar(action_frame)
    self.actionbutton = ttk.Button(action_frame, text = 'Start Process', command=self.run_stitch_process_async)
    self.progress.grid(row = 2, column=0, columnspan=2, pady=(1,5), sticky="new")
    self.actionbutton.grid(row = 2, column = 2, padx=(5,0), pady=(0,5), sticky="new")
    action_frame.columnconfigure(0, weight=1)
    action_frame.columnconfigure(1, weight=1)
    action_frame.columnconfigure(2, weight=1)
    return action_frame

  def advanced_settings_toggle(self, frame, subframe):
    if (self.show_advanced_settings.get()):
      frame.grid(row = 1, column = 0, sticky="new")
    else:
      frame.grid_forget()
      self.show_subprocess_settings.set(self.show_advanced_settings.get())
    self.subprocess_setting_toggle(subframe)
    self.save_app_settings()

  def subprocess_setting_toggle(self, frame):
    if (self.show_subprocess_settings.get()):
      frame.grid(row = 0, column = 1, sticky="news",  padx=(0,10), rowspan=4)
    else:
      frame.grid_forget()
    self.save_app_settings()

  def update_width_mode(self, widthfieldtitle, widthfield):
    self.save_app_settings() 
    enforce_type = self.width_enforce_type.get()
    if enforce_type == 'Automatic Uniform Width':
      widthfieldtitle.grid_remove()
      widthfield.grid_remove()
    elif enforce_type == 'User Customized Width':
      widthfieldtitle.grid(row = 4, column = 0, columnspan=2, sticky="new")
      widthfield.grid(row = 5, column = 0, columnspan=2, pady=(2,0), sticky="new")
    else:
      widthfieldtitle.grid_remove()
      widthfield.grid_remove()

  # These are all the necssary helper functions.
  def browse_input_path(self):
    """Opens Browse Dialog and Gets Directory For the Input and Updates Output."""
    foldername = filedialog.askdirectory()
    self.input_folder.set(foldername)
    self.output_folder.set(foldername + " [Stitched]")

  def browse_subprocess_path(self):
    """Opens Browse Dialog and Gets path For the Subprocess File."""
    filename = filedialog.askopenfilename()
    if ' ' in filename:
      filename = "\"" + filename + "\""
    self.subprocess_path.set(filename)
    self.save_app_settings()

  def update_subprocess_path(self, *args):
    """Opens Browse Dialog and Gets path For the Subprocess File."""
    filename = self.subprocess_path.get()
    if ' ' in filename and not "\"" in filename:
      filename = "\"" + filename + "\""
    elif not ' ' in filename and "\"" in filename:
      filename = filename.replace("\"", "")
    self.subprocess_path.set(filename)
    self.save_app_settings()

  def update_output_path(self, *args):
    """Opens Browse Dialog and Gets Directory For the Input and Updates Output."""
    self.output_folder.set(self.input_folder.get() + " [Stitched]")

  def validate_nums_only(self,P,d,s):
    """Allows only numbers to be written in the Entry Field."""
    if d == '1': 
      if not (P.isdigit()):
        return False
    return True

  def validate_percentage_only(self,P,d,s):
    """Allows only percentages to be written in the Entry Field."""
    if d == '1': 
      if not (P.isdigit() and len(s) < 3 and int(P)<=100):
        return False
    return True

  def validate_onetotwenty_only(self,P,d,s):
    """Allows only percentages to be written in the Entry Field."""
    if d == '1': 
      if not (P.isdigit() and len(s) < 3 and 20>=int(P)>=1):
        return False
    return True

  def update_gui_progress(self, status_message, progress_increase):
    """Updates/Increments the progress value with the given value"""
    self.status.set(status_message)
    self.progress['value'] += progress_increase
    Tk.update_idletasks(self)

  def update_saving_progress(self, num_of_data):
    """Updates the progress value according to the number of files being saved."""
    self.progress['value'] += ((60 * 1/num_of_data) / self.num_of_inputs)
    Tk.update_idletasks(self)

  def update_subprocess_console(self, console_line):
    self.subprocess_console["text"] = self.subprocess_console["text"] + console_line

  def pre_process_check(self):
    """Checks if all the settings and parameters are ready for the operation to start."""
    self.actionbutton['state'] = "disabled"
    if(self.input_folder.get() == ""):
      self.status.set("Idle - No Input folder path given!")
      self.actionbutton['state'] = "normal"
      return False
    if(self.output_folder.get() == ""):
      self.status.set("Idle - No Output folder path set!")
      self.actionbutton['state'] = "normal"
      return False
    if(not os.path.exists(self.input_folder.get())):
      self.status.set("Idle - Input folder path does not exist.")
      self.actionbutton['state'] = "normal"
      return False
    if(self.split_height.get() == "" or self.split_height.get() == "0"):
      self.status.set("Idle - Split Height value was not set!")
      self.actionbutton['state'] = "normal"
      return False
    if(self.slicing_senstivity.get() == ""):
      self.status.set("Idle - Detection Senstivity value was not set!")
      self.actionbutton['state'] = "normal"
      return False
    if(self.ignorable_edges_pixels.get() == ""):
      self.status.set("Idle - Ignoreable Pixels value was not set!")
      self.actionbutton['state'] = "normal"
      return False
    if(self.scan_line_step.get() == ""):
      self.status.set("Idle - Scan Line Step value was not set!")
      self.actionbutton['state'] = "normal"
      return False
    return True

  def stitch_process(self):
    """Runs the stitch process using the SS core functions, and updates the progress on the UI."""
    self.status.set("Working - Loading Image Files!")
    self.progress['value'] = 0
    self.subprocess_console['text'] = ""
    folder_paths = ssc.get_folder_paths(self.enable_batch_mode.get(),self.input_folder.get(), self.output_folder.get())
    # Sets the number of folders as a global variable, so it can be used in other update related functions.
    self.num_of_inputs = len(folder_paths)
    if (self.num_of_inputs == 0):
      return "batch mode no folders"
    for path in folder_paths:
      images = ssc.load_images(path[0])
      if len(images) == 0 and self.num_of_inputs == 1:
        return "no images"
      elif len(images) == 0:
        continue
      # The reason index is used here is because the core functions use intgers to switch between enforcement modes/types
      width_type_index = self.width_enforce_types.index(self.width_enforce_type.get())
      if width_type_index == 0:
        self.update_gui_progress("Working - Combining Image Files!", (10 / self.num_of_inputs))
      else:
        self.update_gui_progress("Working - Resizing & Combining Image Files!", (10 / self.num_of_inputs))
      resized_images = ssc.resize_images(images, width_type_index, self.custom_enforce_width.get())
      combined_image = ssc.combine_images(resized_images)
      self.update_gui_progress("Working - Slicing Combined Image into Finalized Images!", (10 / self.num_of_inputs))
      final_images = ssc.split_image(combined_image, self.split_height.get(), self.slicing_senstivity.get(), self.ignorable_edges_pixels.get(), self.scan_line_step.get())
      self.update_gui_progress("Working - Saving Finalized Images!", (20 / self.num_of_inputs))
      # The reason a function called update_saving_progress is passed is so the UI can be updated about the saving progress
      # since it is one of the longest, if not the longest stage in this process.
      ssc.save_data(final_images, path[1], self.output_files_type.get(), self.update_saving_progress)
      if (self.enable_subprocess_execution.get()):
        self.status.set("Working - Running Subprocess on Finalized Images!")
        processed_path = path[1]+ " [Processed]"
        command = self.subprocess_path.get() + " " + self.subprocess_arguments.get()
        command = command.replace('[stitched]', "\"" + path[1]+ "\"")
        command = command.replace('[processed]', "\"" + processed_path + "\"")
        ssc.call_external_func(command, self.update_subprocess_console, processed_path)
    return "complete"

  def run_stitch_process(self):
    if (self.pre_process_check() == False):
      return
    process_status = ""
    starting_time = time()
    try:
      process_status = self.stitch_process()
    except Exception as e:
      logging.exception("An unexpected error has occured at " + str(datetime.now()))
      process_status = "crash"
    ending_time = time()
    delta = ending_time - starting_time
    if (process_status == "crash"):
      self.status.set("Idle - An Unexpected Error Occured, Check The'crashreport.log' File!")
    elif (process_status == "batch mode no folders"):
      self.status.set("Idle - Batch Mode Enabled, No Suitable Input Folders Found!")
    elif (process_status == "no images"):
      self.status.set("Idle - No Image Files Found!")
    else:
      self.status.set("Idle - Files successfully stitched in " +  str(delta) + "sec!")
    self.progress['value'] = 0
    self.actionbutton['state'] = "normal"
  
  def run_stitch_process_async(self, *args):
    workthread = threading.Thread(target=self.run_stitch_process)
    workthread.start()
        

SmartStitchGUI().mainloop()
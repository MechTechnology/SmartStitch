class WorkDirectory:
    """Model for holding Working Directory Information"""

    def __init__(self, input, output, postprocess):
        # Initialize the WorkDirectory object with input, output, and postprocess paths.
        # 'input' is the path to the input files directory.
        # 'output' is the path to the output files directory.
        # 'postprocess' is the path to the postprocess files directory.
        self.input_path: str = input
        self.output_path: str = output
        self.postprocess_path: str = postprocess
        self.input_files: list = []   # Initialize an empty list to store input files.
        self.output_files: list = []  # Initialize an empty list to store output files.

    # This method dictates how the object will be represented in the log file.
    def __repr__(self):
        stringRep = "\'input_path=" + str(self.input_path)

        # If there are input files, add their count to the representation.
        if self.input_files:
            stringRep += ", input_files:" + str(len(self.input_files))

        # Add the output_path to the representation.
        stringRep += ", output_path:" + str(self.output_path)

        # If there are output files, add their count to the representation.
        if self.output_files:
            stringRep += ", output_files:" + str(len(self.output_files))

        # Add the postprocess_path to the representation.
        stringRep += ", postprocess_path=" + str(self.postprocess_path)

        stringRep += "\'"
        return stringRep
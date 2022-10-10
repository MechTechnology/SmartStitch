class WorkDirectory:
    """Model for holding Working Directory Information"""

    def __init__(self, input, output, postprocess):
        self.input_path: str = input
        self.output_path: str = output
        self.postprocess_path: str = postprocess
        self.input_files: list = []
        self.output_files: list = []

    # This dictates how it will look in the log file.
    def __repr__(self):
        stringRep = "\'input_path=" + str(self.input_path)
        if self.input_files:
            stringRep += ", input_files:" + str(len(self.input_files))
        stringRep += ", output_path:" + str(self.output_path)
        if self.output_files:
            stringRep += ", output_files:" + str(len(self.output_files))
        stringRep += ", postprocess_path=" + str(self.postprocess_path)
        stringRep += "\'"
        return stringRep

import os
from natsort import natsorted
from ..models import WorkDirectory
from ..utils.constants import OUTPUT_SUFFIX, POSTPROCESS_SUFFIX, SUPPORTED_IMG_TYPES
from ..utils.errors import DirectoryException
from .global_logger import logFunc


class DirectoryExplorer:
    def run(self, input, **kwargs):
        """
        This method is the entry point for running the DirectoryExplorer.
        It takes an input path and other optional keyword arguments and returns a list of working directories.
        """
        main_directory = self.get_main_directory(input, **kwargs)
        working_directories = self.explore_directories(main_directory)
        return working_directories

    def create_directory(self, path):
        """
        Creates a directory at the specified path if it doesn't exist.
        """
        os.makedirs(path, exist_ok=True)

    @logFunc(inclass=True)
    def get_main_directory(self, input: str, **kwargs: str) -> WorkDirectory:
        """
        Gets the main working directory for a given input path.
        It takes the input path as a parameter and optional keyword arguments (output and postprocess paths).
        It returns a WorkDirectory object that represents the main working directory.
        """
        if not input:
            raise DirectoryException("Missing Input Directory")
        input_path = os.path.abspath(input)
        output_path = kwargs.get('output_path', input_path + OUTPUT_SUFFIX)
        postprocess_path = kwargs.get('postprocess', input_path + POSTPROCESS_SUFFIX)
        return WorkDirectory(input_path, output_path, postprocess_path)

    @logFunc(inclass=True)
    def explore_directories(self, main_directory: WorkDirectory) -> list[WorkDirectory]:
        """
        Gets all the possible working directories from main paths.
        It takes a main_directory (a WorkDirectory object) as input and returns a list of WorkDirectory objects.
        It explores the main directory and its subdirectories to find possible working directories containing image files.
        """
        work_directories = []
        for (dir_root, folders, files) in os.walk(main_directory.input_path, topdown=True):
            # Traverse through all directories and subdirectories in the main_directory.
            img_files = [file for file in files if file.lower().endswith(SUPPORTED_IMG_TYPES)]
            img_files = natsorted(img_files)  # Sort the image files in natural order.
            if img_files:
                # If there are image files in the current directory, create a WorkDirectory object to represent it.
                rel_root = os.path.relpath(dir_root, main_directory.input_path)
                dir_output = os.path.join(main_directory.output_path, rel_root)
                dir_subprocess = os.path.join(main_directory.postprocess_path, rel_root)
                directory = WorkDirectory(dir_root, dir_output, dir_subprocess)
                directory.input_files = img_files
                work_directories.append(directory)
        if not work_directories:
            # If no valid work directories with image files were found, raise an exception.
            raise DirectoryException('No valid work directories were found!')
        return work_directories

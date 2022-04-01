from os import path, walk
from typing import List

from natsort import natsorted

from core.models.work_directory import WorkDirectory
from core.services.global_logger import logFunc
from core.utils.constants import OUTPUT_SUFFIX, SUBPROCESS_SUFFIX, SUPPORTTED_IMG_TYPES
from core.utils.errors import DirectoryException


class DirectoryExplorer:
    def run(self, input, **kwargs):
        main_directory = self.get_main_directory(input, **kwargs)
        working_directories = self.explore_directories(main_directory)
        return working_directories

    @logFunc(inclass=True)
    def get_main_directory(self, input: str, **kwargs: str) -> WorkDirectory:
        """Gets the main working directory for a given input path"""
        input_path = path.abspath(input)
        output_path = kwargs.get('output', input_path + OUTPUT_SUFFIX)
        subprocess_path = kwargs.get('output', input_path + SUBPROCESS_SUFFIX)
        return WorkDirectory(input_path, output_path, subprocess_path)

    @logFunc(inclass=True)
    def explore_directories(self, main_directory: WorkDirectory) -> List[WorkDirectory]:
        """Gets all the possible working directories from main paths"""
        work_directories = []
        for (dir_root, folders, files) in walk(main_directory.input_path, topdown=True):
            img_files = []
            for file in files:
                if file.lower().endswith(SUPPORTTED_IMG_TYPES):
                    img_files.append(file)
            img_files = natsorted(img_files)
            if img_files:
                rel_root = path.relpath(dir_root, main_directory.input_path)
                dir_output = path.join(main_directory.output_path, rel_root)
                dir_subprocess = path.join(main_directory.subprocess_path, rel_root)
                directory = WorkDirectory(dir_root, dir_output, dir_subprocess)
                directory.input_files = img_files
                work_directories.append(directory)
        if not (work_directories):
            raise DirectoryException('No valid work directories were found!')
        return work_directories

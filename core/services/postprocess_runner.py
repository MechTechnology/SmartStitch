import os
import subprocess

from core.models.work_directory import WorkDirectory
from core.services.global_logger import logFunc


class PostProcessRunner:
    def run(self, workdirectory: WorkDirectory, **kwargs: dict[str:any]):
        command = (
            "\""
            + kwargs.get("postprocess_app", "")
            + "\" "
            + kwargs.get("postprocess_args", "")
        )
        console_func = kwargs.get("console_func", print)
        command = command.replace('[stitched]', "\"" + workdirectory.output_path + "\"")
        command = command.replace(
            '[processed]', "\"" + workdirectory.postprocess_path + "\""
        )
        return self.call_external_func(
            workdirectory.postprocess_path, command, console_func
        )

    @logFunc(inclass=True)
    def call_external_func(self, processed_path, command, console_func):
        if not os.path.exists(processed_path):
            os.makedirs(processed_path)
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf-8',
            errors='replace',
            universal_newlines=True,
            shell=True,
        )
        console_func("Post process started!\n")
        for line in proc.stdout:
            console_func(line)
        # for line in proc.stderr:
        #   print_func(line)
        console_func("\nPost process finished successfully!\n")
        proc.stdout.close()
        return_code = proc.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, command)

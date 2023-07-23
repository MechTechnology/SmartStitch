import os
import subprocess
from core.models.work_directory import WorkDirectory
from core.services.global_logger import logFunc

class PostProcessRunner:
    def run(self, workdirectory: WorkDirectory, **kwargs: dict[str:any]):
        # Construct the post-process command based on input parameters
        postprocess_app = kwargs.get("postprocess_app", "")
        postprocess_args = kwargs.get("postprocess_args", "")
        command = f'"{postprocess_app}" {postprocess_args}'

        # Get the provided console function or use print as the default
        console_func = kwargs.get("console_func", print)

        # Replace placeholders in the command with appropriate paths
        command = command.replace('[stitched]', f'"{workdirectory.output_path}"')
        command = command.replace('[processed]', f'"{workdirectory.postprocess_path}"')

        # Call the external function and return its result
        return self.call_external_func(workdirectory.postprocess_path, command, console_func)

    # Decorator to log function calls in the class
    @logFunc(inclass=True)
    def call_external_func(self, processed_path, command, console_func):
        # Create the processed_path directory if it doesn't exist
        os.makedirs(processed_path, exist_ok=True)

        # Launch the subprocess with the provided command
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf-8',
            errors='replace',
            universal_newlines=True,
            shell=True,
        )

        # Inform that the post-process has started
        console_func("Post process started!\n")

        # Capture and print the subprocess output line by line using the console_func
        for line in proc.stdout:
            console_func(line)

        # Uncomment the following lines if you want to capture and print stderr as well
        # for line in proc.stderr:
        #     console_func(line)

        # Inform that the post-process has finished successfully
        console_func("\nPost process finished successfully!\n")

        # Close the stdout pipe and wait for the subprocess to finish
        proc.stdout.close()
        return_code = proc.wait()

        # If the return code is non-zero, raise a CalledProcessError
        if return_code:
            raise subprocess.CalledProcessError(return_code, command)
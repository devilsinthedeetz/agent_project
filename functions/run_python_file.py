import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_file: bool = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_file:
            raise Exception(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_file):
            raise Exception(f'Error: "{file_path}" does not exist or is not a regular file')
        if not target_file.endswith('.py'):
            raise Exception(f'Error: "{file_path}" is not a Python file')
        command: list[str] = ["python", target_file]
        command_output: str = ""
        if args:
            command.extend(args)
        completed_process = subprocess.run(command, capture_output=True, timeout=30, text=True)
        if completed_process.returncode != 0:
            command_output += f"\nProcess exited with code {completed_process.returncode}"
        if not completed_process.stdout and not completed_process.stderr:
            command_output += f"\nNo output produced"
        if completed_process.stdout:
            command_output += "\n" + "STDOUT:" + completed_process.stdout
        if completed_process.stderr:
            command_output += "\n" + "STDERR:" + completed_process.stderr
        return command_output
    except Exception as e:
        return e

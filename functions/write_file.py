import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_file: bool = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_file:
            raise Exception(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        if os.path.isdir(target_file):
            raise Exception(f'Error: Cannot write to "{file_path}" as it is a directory')
        print(f"{target_file}")
    except Exception as e:
        return e

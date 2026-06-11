import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_dir: bool = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_dir:
            raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(target_dir):
            raise Exception(f'Error: "{directory}" is not a directory')

        def files_info(target_dir_files: list[str], target_dir: str) -> str:
            file_strings: list[str] = []
            for file in target_dir_files:
                file_path: str = os.path.normpath(os.path.join(target_dir, file))
                file_strings.append(f"  - {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}")
            return '\n'.join(file_strings)

        def dir_desc(directory: str, target_dir: str, working_dir_abs: str) -> str:
            if target_dir == working_dir_abs:
                return "current directory"
            else:
                return f"'{directory}'"


        return f"""Results for {dir_desc(directory, target_dir, working_dir_abs)} directory:
{files_info(os.listdir(target_dir), target_dir)}
"""
    except Exception as e:
        return e

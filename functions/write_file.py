import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write file contents into a new file, or overwrite existing contents of a file, with a file path relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write file contents into, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Contents that will be written to the file."
            )
        },
        required=["file_path", "content"],
        propertyOrdering=["file_path", "content"]
    ),
)

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_file: bool = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_file:
            raise Exception(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        if os.path.isdir(target_file):
            raise Exception(f'Error: Cannot write to "{file_path}" as it is a directory')
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return e

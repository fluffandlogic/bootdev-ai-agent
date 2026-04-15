import os
from google import genai
from google.genai import types
from config import MAX_CHARS

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to write file to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to file",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):

    working_directory_abs = os.path.abspath(working_directory)
    target = os.path.normpath(os.path.join(working_directory_abs, file_path))
    valid_target = os.path.commonpath([working_directory_abs, target]) == working_directory_abs

    if not valid_target:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    dirname = os.path.dirname(target)
    os.makedirs(dirname, exist_ok=True)

    with open(target, "w") as file:
        try:
            file.write(content)
        except Exception:
            return f'Error: {Exception()}'
        else:
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        


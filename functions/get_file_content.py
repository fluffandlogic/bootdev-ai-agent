import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):

    working_directory_abs = os.path.abspath(working_directory)
    target = os.path.normpath(os.path.join(working_directory_abs, file_path))
    valid_target = os.path.commonpath([working_directory_abs, target]) == working_directory_abs

    if not valid_target:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(target, "r") as file:
        try:
            content = file.read(MAX_CHARS)
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
        except Exception as e:
            return f"Error: {e}"



    
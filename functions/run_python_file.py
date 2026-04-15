import os
import subprocess
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes Python file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to Python file, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Name of Python file to execute",
                items=types.Schema(type=types.Type.STRING)
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    working_directory_abs = os.path.abspath(working_directory)
    target = os.path.normpath(os.path.join(working_directory_abs, file_path))
    valid_target = os.path.commonpath([working_directory_abs, target]) == working_directory_abs

    if not valid_target:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    filename, extension = os.path.splitext(target)
    if extension != '.py':
        return f'Error: "{file_path}" is not a Python file'

    command = ["Python3", target]
    if args:
        command.extend(args)
    
    try:
        completed_process = subprocess.run(command, stdout=True, stderr=True, timeout=30, text=True) 
    except Exception as e:
        return f"Error: executing Python file: {e}"
    else:
        output = ""
        if completed_process.returncode != 0:
            output += f"Process exited with code {completed_process.returncode}\n"

        if not completed_process.stdout:
            output += "STDOUT: " + "No output produced\n"
        else:
            output += "STDOUT: " + completed_process.stdout + "\n"

        if not completed_process.stderr:
            output += "STDERR: " + "No output produced\n"
        else:
            output += "STDERR: " + completed_process.stderr + "\n"

        return output
        


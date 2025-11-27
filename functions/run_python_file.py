import subprocess
import os
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'
    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    if args is None:
        args = []
    try:
        cmd = ['python', file_path] + list(args)
        completed = subprocess.run(cmd, timeout=30, 
                    capture_output=True, 
                    cwd=abs_working_dir, 
                    text=True)

        stdout = completed.stdout or ""
        stderr = completed.stderr or ""

        if not stdout and not stderr:
            return "No output produced"
        result = f"STDOUT: {stdout}\n"+ f"STDERR: {stderr}"
        if completed.returncode != 0:
            result += f"Process exited with code {completed.returncode}"
        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the file specifed by the file_path argument. This function should be constrained to the working directory and should pass arguments to a function if there are any",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="This is a list that will hold the arguments that are to be passed to the target function",
            ),
        },
    ),
)

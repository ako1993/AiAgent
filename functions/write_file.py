import os

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:  
        dir_name = os.path.dirname(target_file)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
    
        with open(target_file, "w") as t:
            t.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'

    
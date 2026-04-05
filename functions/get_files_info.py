import os

def get_files_info(working_directory, directory="."):
    
    working_directory_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))
    valid_target_dir = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs

    if not os.path.isdir(target_dir):
        return f'Error: "{directory} is not a directory'

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    dir_contents = os.listdir(target_dir)

    dir_contents_summary = ""
    for content in dir_contents:
        content_full_path = os.path.join(target_dir, content)
        content_is_dir = os.path.isdir(content_full_path)
        content_file_size = os.path.getsize(content_full_path)
        dir_contents_summary += (f"- {content}: file_size={content_file_size} bytes, is_dir={content_is_dir}\n")

    return dir_contents_summary
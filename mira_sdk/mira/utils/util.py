import os


def split_name(name):
    parts = name.split('/')
    if len(parts) < 2:
        raise ValueError(f"Invalid name: {name}")
    org, name = parts[0].lstrip('@'), parts[1]
    return org, name


def check_file_path(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"The file {file_path} is not readable.")

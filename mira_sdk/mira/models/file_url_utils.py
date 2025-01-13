import os
import re

class Reader:
    def __init__(self, url: str):
        pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)$'
        if not re.match(pattern, url):
            raise ValueError("Invalid URL format")
        self.url = url
    
    def __str__(self):
        return self.url

class File:
    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise ValueError(f"File path does not exist: {file_path}")
        if not os.path.isfile(file_path):
            raise ValueError(f"Path is not a file: {file_path}")
            
        self.file_path = file_path

    def __str__(self):
        return self.file_path

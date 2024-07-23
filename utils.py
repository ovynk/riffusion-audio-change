import os
import re


def get_files_by_regex(regex: str, directory: str):
    regex = re.compile(regex)
    files = []

    for f in os.listdir(directory):
        if regex.match(f) is not None:
            files.append(f)

    return files

# app/cleanup/utils.py

import os
from datetime import datetime


def get_file_age_in_days(file_path):
    """
    Returns age of file in days
    """
    file_mtime = os.path.getmtime(file_path)
    file_date = datetime.fromtimestamp(file_mtime)
    age = (datetime.now() - file_date).days
    return age


def is_file(file_path):
    """
    Check if path is a file (not directory)
    """
    return os.path.isfile(file_path)
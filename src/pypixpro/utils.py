import os
import sys


def get_resource_path(relative_path):
    """
    Get the absolute path to a resource, working for both development
    and PyInstaller frozen builds.
    """
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        # In development, we are in src/pypixpro/utils.py (or similar depth)
        # We need to go up two levels to reach the project root if this file is in src/pypixpro/
        # root/src/pypixpro/utils.py -> root/
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    return os.path.join(base_path, relative_path)

import subprocess
import sys
import os

def open_folder(path: str):
    if not os.path.isdir(path):
        print(f"Error: Directory not found at {path}")
        return

    try:
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.run(["open", path])
        else: # linux
            subprocess.run(["xdg-open", path])
    except Exception as e:
        print(f"Error opening folder: {e}")
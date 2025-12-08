"""cleaner.py

Allows you to clear the terminal.
"""

import os
import sys


def check_os() -> str:
    """Check user's OS

    Returns:
        str: The name of the command to clear the terminal.
    """
    if sys.platform.startswith("win"):
        return "cls"
    if sys.platform.startswith("darwin"):
        return "clear"
    if sys.platform.startswith("linux"):
        return "clear"
    return ""

def clean() -> None:
    """Clears the terminal of unnecessary text."""
    clear_command = check_os()
    if clear_command:
        os.system(clear_command)
    else:
        print(
            "The full functionality of the program is supported only on: Linux, macOS, Windows."
        )
    

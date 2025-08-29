"""cleaner.py

Позволяет очистить терминал.
"""

import os
import sys


def clean() -> None:
    """Чистит терминал от текста"""

    is_windows = sys.platform.startswith("win")
    is_mac = sys.platform.startswith("darwin")
    is_linux = sys.platform.startswith("linux")

    clear_command = ""

    if is_windows:
        clear_command = "cls"
    elif is_mac:
        clear_command = "clear"
    elif is_linux:
        clear_command = "clear"
    else:
        print(
            "Полный фунционал программы поддерживается только на: Linux, macOS, Windows."
        )

    os.system(clear_command)

"""
A module that checks for user modules inside the "user" directory
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # /Prometheus
USER_LIB = os.path.join(BASE_DIR, "user")  # Prometheus/user


# Reminder: Dictionary is a mutable data type.
ALLOWED_MODULES = {"prompts": False, "actions": False, "patterns": False}


def scan_user_overrides() -> None:
    """
    Checks the "user" directory for overriding modules.

    Sets flags in ALLOWED_MODULES.
    """
    if not os.path.isdir(USER_LIB):
        return

    for entry in os.scandir(USER_LIB):
        if entry.is_file() and entry.name.endswith(".py"):
            name = entry.name[:-3]  # without .py
            if name in ALLOWED_MODULES:
                ALLOWED_MODULES[name] = True


# Start scanning on import
scan_user_overrides()

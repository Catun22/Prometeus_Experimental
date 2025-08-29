"""
Содержит небольшую утилиту для открытия файлов json.
"""

from typing import Any
import json


def open_json(file: str) -> Any:
    """Открывает файл .json"""
    with open(file, "r", encoding="utf-8") as f:
        json_file = json.load(f)
        return json_file

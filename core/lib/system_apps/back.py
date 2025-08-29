"""
Создает бэкапы для словаря.
"""

import os
import shutil
from datetime import datetime
from core.utilits.opener_json import open_json

def cleanup_backups(backup_dir: str, max_backups: int = 5):
    """Оставляем только последние max_backups файлов"""
    files = sorted(
        (os.path.join(backup_dir, f) for f in os.listdir(backup_dir)),
        key=os.path.getmtime
    )
    while len(files) > max_backups:
        os.remove(files[0])
        files.pop(0)

def backup(max_backups: int = 5):
    """Создать резервную копию словаря"""
    # Ищем config.json на 4 папки выше
    current_file = os.path.abspath(__file__)
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file))))
    config_path = os.path.join(base_path, "config.json")
    config = open_json(config_path)

    paths = config["paths"]
    md_file = paths["dictionary"]
    backup_dir = paths["backup"]
    # создаём директории для словаря (если их нет)
    os.makedirs(os.path.dirname(md_file), exist_ok=True)
    # создаём директории для бэкапов (если их нет)
    os.makedirs(backup_dir, exist_ok=True)

    if not os.path.exists(md_file):
        print(f"[{datetime.now()}] Файл словаря не найден: {md_file}")
        return

    os.makedirs(backup_dir, exist_ok=True)

    # имя копии с датой и временем
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"dictionary_{timestamp}.md")

    shutil.copy2(md_file, backup_file)
    print(f"[{datetime.now()}] Резервная копия создана: {backup_file}")

    cleanup_backups(backup_dir, max_backups)

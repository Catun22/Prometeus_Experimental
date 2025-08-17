"""installer.py 

Позволяет установить colorama для Windows.
"""
import subprocess


def install() -> None:
    """Устанавливает библиотку colorama"""

    prompt = (
    "Библиотека colorama не установлена.\n"
    "ANSI escape code может не поддерживаться.\n"
    "Установите colorama через pip install.\n"
    )
    try:
        from colorama import just_fix_windows_console
        just_fix_windows_console()
    except ImportError:
        print(prompt)

    prompt = "Установить библиотеку colorama? [Y/N]\n>>> "

    try:
        import colorama   # type: ignore
        print("Colorama установлена.")
        return
    except ImportError:
        pass

    while True:
        entry = input(prompt)

        if entry.lower() == "y":
            subprocess.run(["pip", "install", "colorama"])
            print("Установка завершена")
            break
        elif entry.lower() == "n":
            break
        else:
            print("Неверный ввод, попробуйте снова")

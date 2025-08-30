"""
Точка входа в проект Prometheus.

Назначение:
    - Инициализирует приложение
    - Настраивает меню
    - Запускает главный цикл программы
"""

from rich.console import Console

from core.menu import Menu
from core.lib.actions import CLI
from core.lib.prompts import Prompts
from core.utilits.opener_json import open_json
from core.utilits.cleaner import clean
from core.utilits.installer import install


menu_name = "МЕНЮ"
file_path = __file__
dir_path = os.path.dirname(file_path)
menu_config = os.path.join(dir_path, "menu.json")


def main():
    welcome()
    set_menu_cli()


def welcome():
    console = Console()
    clean()
    install()
    console.print(Prompts.welcome)


def set_menu_cli():
    cli = CLI()
    actions_config = open_json(cli.actions_path)
    ACTIONS = {
        key: getattr(cli, method_name) for key, method_name in actions_config.items()
    }

    menu_structure = open_json(menu_config)
    menu = Menu(menu_name, menu_structure, ACTIONS)
    menu.start()


if __name__ == "__main__":
    main()


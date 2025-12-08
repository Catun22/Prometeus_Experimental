"""
The entry point for the Prometheus project.

Purpose:
    - Initializes the application
    - Configures the menu
    - Starts the main program loop
"""

# Regular imports
from rich.console import Console
from core.menu import Menu

from core.utilits.opener_json import open_json
from core.utilits.cleaner import clean
from core.utilits.installer import install
from core.utilits.error_catcher import error_print

# The logic for connecting user modules
from core import loader
if loader.ALLOWED_MODULES.get("actions", False):
    from user.actions import MyCLI
    cli = MyCLI()
else:
    from core.lib.actions import CLI
    cli = CLI()

if loader.ALLOWED_MODULES.get("prompts", False):
    from user import prompts as p
else:
    from core.lib.prompts import prompts_menu as p


###-$ BOTTOM UP $-###


def welcome() -> None:
    """Clears and colors the terminal. Displays the program title."""
    clean()
    install()
    console = Console()
    welcome = p.UserPrompts()
    console.print(welcome.welcome)


def set_menu_cli(menu_name: str) -> None:
    """Sets the menu - settings, structure and functions"""
    actions_config: dict[str, str] = open_json(cli.actions_path)
    ACTIONS = {
        key: getattr(cli, method_name) for key, method_name in actions_config.items()
    }

    menu_structure = open_json(cli.menu_path)
    menu = Menu(menu_name, menu_structure, ACTIONS)
    menu.start()


def main() -> None:
    """Entry point into the program"""
    menu_name = "МЕНЮ"
    welcome()
    try:
        set_menu_cli(menu_name)
    except AttributeError as e:
        error_print(e)

if __name__ == "__main__":
    main()

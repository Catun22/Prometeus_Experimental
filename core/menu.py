"""

A module containing the program menu.

"""

from typing import Callable, Union, TypeAlias

from rich.text import Text
from rich.console import Console
from core.lib.prompts import prompts_system as ps

from core import loader

if loader.ALLOWED_MODULES.get("prompts", False):
    from user.prompts import UserPrompts
else:
    from core.lib.prompts.prompts_menu import UserPrompts

MenuStructure: TypeAlias = dict[
    str, Union[str, "MenuStructure"]
]  # A thing that makes annotations.
# The menu contains a so-called "recursive dictionary" - a dictionary within a dictionary, within which there is another dictionary, dictionary, dictionary...
# The interpreter will "walk" through the dictionaries, as if "along branches",
#  until at the end the interpreter comes across a stub or some action (or rather, a link that is tied to a function).
# (To put it very simply, until the interpreter encounters a function name,
#  we'll check for its existence and try to call it using () such brackets (or via .__call__() ).


class Menu:
    """Recursive menu

    Args:
        title (str | None, optional): Name for the menu title.. Defaults to None.
        structure (MenuStructure | None, optional): Menu structure. Can be nested at any depth.. Defaults to None.
        actions (dict[str, Callable[[], None]] | None, optional): A dictionary containing names of functions to call. Defaults to None.
    """

    def __init__(
        self,
        title: str | None = None,
        structure: MenuStructure | None = None,
        actions: dict[str, Callable[[], None]] | None = None,
    ) -> None:

        self.__console = Console()
        self.__support_console = Console(width=30)
        self.__up = UserPrompts()

        self.__title = title if title is not None else "Menu name"
        self.__history_title: list[str] = [self.__title]
        self.__structure: MenuStructure = (
            structure
            if structure is not None
            else {"Point 1": {}, "Point 2": {}, "Point 3": {}}
        )
        self.__stack = [self.__structure]  # to go back
        self.__actions: dict[str, Callable[[], None]] = actions or {}
        # self.stack will store the "history" of the menu or items we have selected.
        # Thanks to this thing we can "go back".

    def __container(self) -> None:
        """Contains the main menu of the cycle"""
        # As long as we have any items on the menu:
        while self.__stack:
            self.__current = self.__stack[-1]  # current menu
            options = list(self.__current.keys())
            self.__display_menu(self.__title, options)

            # take user's choice
            self.__console.print(self.__up.choise)
            choice = self.__console.input(ps.Prompts.arrows)
            exit_flag = self.__choice_handler(options, choice)  # Returns True if "Exit"
            if exit_flag:  # Breaking the cycle
                break

    def __check_choice(self, choice: str) -> int | str | None:
        """Checks if the user input is a number.

        Args:
            choice (str): A user-entered number as a string, or just a string.

        Returns:
            int | None: int if the user entered a number. None if the user entered anything other than a number.
        """

        if choice.lower() in ("q", "b"):
            return choice.lower()

        if not choice.isdigit():
            return None
        index = int(choice)
        if not self.__current or not (1 <= index <= len(self.__current)):
            return None
        return index

    def __choice_handler(self, options: list[str], choice: str) -> bool:
        """Processes user selection.

        Args:
            options (list[str]): List of menu items
            choice (str): User's choice.

        Returns:
            bool: False - continue the loop. True - terminate.
        """

        index = self.__check_choice(choice)
        if index is None:
            self.__console.print(ps.PromptsMenu.bad_entry)
            return False  # Incorrect input, the cycle continues

        if index == "b":  # If the user selected "Back":
            if (
                len(self.__stack) > 1
            ):  # If there are any menus left in the menu history and we haven't reached the very first, main menu.
                self.__stack.pop()
                self.__history_title.pop()
                self.__title = self.__history_title[-1]
            else:  # We are in the main menu, continuing the cycle
                self.__console.print(ps.PromptsMenu.main_menu)
            return False
        elif index == "q":  # Exit - return True, the loop is broken
            self.__console.print(ps.PromptsMenu.exit)
            return True
        else:  # In other cases (when selecting another menu or action/stub)
            selected = options[
                int(index) - 1
            ]  # We coordinate the indices so that the correct option is selected, and not +1
            sub = self.__current[
                selected
            ]  # In the dictionary we find a key named selected
            if isinstance(sub, dict):  # If there is a dictionary inside:
                self.__stack.append(sub)  # Add a new menu to the menu history (stack).
                self.__history_title.append(selected)
                self.__title = selected
            # If the key inside is a string, and the value inside is a function reference.
            else:
                action = self.__actions.get(sub)
                if action:  # Perform the action
                    action()
                else:  # If there is neither a dictionary nor a function, but a stub
                    # We are simply notifying that the stub is working, but the function itself has not yet been implemented.
                    self.__console.print(f"{ps.PromptsMenu.perform_action} {selected}")
            return False  # We continue the cycle

    def __display_title(self, title: str) -> None:
        """Draws the title page

        Args:
            title (str): Title page name.
        """

        self.__support_console.rule(
            f"[{ps.main_color}]{title}[/{ps.main_color}]", style=ps.second_color
        )  # Let's draw the title card

    def __display_menu(self, title: str, structure: list[str]) -> None:
        """Draws the menu.

        Args:
            title (str): Title page name.
            structure (list[str]): List of menu keys.
        """
        if not structure:
            self.__console.print("Menu is empty")
        self.__display_title(title)
        for number, item in enumerate(structure, 1):
            self.__console.print(
                Text(f"{number}. ", style=f"{ps.support_color}")
                + Text(item, style=ps.main_color)
            )

        self.__console.print()
        self.__console.print(ps.PromptsMenu.back, end=" | ")
        self.__console.print(ps.PromptsMenu.exit)

    def start(self) -> None:
        """Launches menu"""
        self.__container()

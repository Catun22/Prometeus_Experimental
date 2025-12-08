"""
A module containing basic methods for working with templates.
"""
from typing import Any, TypeVar

from rich.text import Text
from core.lib.path_manager import PathManager
from core.lib.templates.patterns import *
from core.lib.helper.helpers import Helper
from core.lib.prompts.prompts_system import Prompts, main_color, support_color

# For the annotation
TemplateClass = TypeVar("TemplateClass", bound="TemplateMd")


class TemplatesHandler():
    """
    A class containing methods for working with classes.

    These methods are present in the CLI class.
    """
    def __init__(self) -> None:
        __pm = PathManager()
        self.menu_path = __pm.get_menu_path()
        self.config_path = __pm.get_config_path()
        self.actions_path = __pm.get_actions_path()
        self.color_path = __pm.get_color_path()
        self.__paths = __pm.paths

        self.hp = Helper()
        # Output colored text
        self.console = self.hp.console

    def create_item(self, *, cls: type[TemplateClass], title_prompt: Text | str, path_key: str, extra_arguments: list[tuple[str, Text]] | None = None) -> None:
        """The method that creates the template

        Args:
            cls (type[TemplateClass]): The template class (from patterns.py )
            title_prompt (Text | str): Prompt is an input prompt.
            path_key (str): The key used to search for the default path in the `config.json` file.
            extra_arguments (list[tuple[str, Text]] | None, optional): Additional arguments as needed. Defaults to None.
        """
        # Requesting the name
        self.console.print(title_prompt)
        title = self.console.input(Prompts.arrows)
        # Requesting tags
        tags = self.__input_tags()
        # Additional fields
        extra_args: dict[str, Any] = {}
        if extra_arguments:
            for field_name, prompt in extra_arguments:
                self.console.print(prompt)
                value = self.console.input(Prompts.arrows).strip() or None
                extra_args[field_name] = value
        
        # Creating an object
        item: TemplateClass = cls(title=title, tags=tags, **extra_args)
        # Default path and save
        self.console.print(Prompts.save, Prompts.file_name, Prompts.save_path, Prompts.enter, Prompts.default)
        item.set_default_path(self.__paths[path_key])
        path_name = self.console.input(Prompts.arrows) or None
        item.start(path_name)
        file_path = item.get_path()
        self.console.print("\nОткрыть файл сейчас (y/n)?")
        if self.console.input(Prompts.arrows).strip().lower() == "y":
            self.hp.support_open_app(file_path)

    def look_item(self, *, cls: type[TemplateClass], path_key: str) -> None:
        """A method that looks through the contents in a directory with templates and outputs them to the terminal.

        Args:
            cls (type[TemplateClass]): The template class (from patterns.py )
            path_key (str): The key used to search for the default path in the `config.json` file.
        """
        item = cls() # Creating a new instance of the class.
        directory = self.__paths[path_key]
        md_files = item.get_available_files(directory) # The default path should also be added here.
        if not md_files:
            self.console.print("Файлы не найдены")
            return
        self.__support_md_loop(md_files)
        while True:
            self.console.print("\nВведите номер файла для открытия или '0' для выхода:")
            choice = self.console.input(Prompts.arrows).strip()

            if choice == "0":
                break

            if not choice.isdigit():
                self.console.print("Введите корректное число")
                continue

            choice = int(choice)
            if 1 <= choice <= len(md_files):
                filepath = os.path.join(directory, md_files[choice - 1])
                self.hp.support_open_app(filepath)  # Open the selected file
            else:
                self.console.print("Неверный выбор")

    def __input_tags(self, prompt: Text = Prompts.tags, input_prompt: Text = Prompts.arrows) -> list[str] | None:
        """Method requesting tags

        Args:
            prompt (Text, optional): Colored prompt. Defaults to Prompts.tags.
            input_prompt (Text, optional): Prompt for input (>>> ).. Defaults to Prompts.arrows.

        Returns:
            list[str] | None: List of tags
        """
        self.console.print(prompt)
        tags: list[str] | None = []
        while True:
            tag = self.console.input(input_prompt).strip()
            if not tag:
                break
            tags.append(tag)
        
        return tags or None
    
    def __support_md_loop(self, md_files: list[str]) -> None:
        """Colors the numbers in a loop."""
        for item, names in enumerate(md_files, 1):
            self.console.print(Text(f"{item}. ", style=support_color) + Text(names, style=main_color))

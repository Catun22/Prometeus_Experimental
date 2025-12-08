"""
A module containing methods that open websites and files.
"""

import sys
import shutil
import subprocess

from rich.console import Console

from core.lib.prompts.prompts_system import Prompts, PromptSite, PromptsHelper, PromptsMenu


class Helper():
    def __init__(self) -> None:
        self.__linux = sys.platform.startswith("linux")
        self.__darwin = sys.platform.startswith("darwin")
        self.__windows = sys.platform.startswith("win")
        self.console = Console()
    
    def support_page(self, link: str) -> None:
        """An auxiliary method for opening web pages in a browser."""
        command = link
        if self.__windows:
            subprocess.Popen(f"start {command}", shell=True, stderr=subprocess.DEVNULL)
        elif self.__darwin:
            subprocess.Popen(f"open {command}", shell=True, stderr=subprocess.DEVNULL)
        elif self.__linux:
            subprocess.Popen(f"bash -c 'xdg-open {command}'", shell=True, stderr=subprocess.DEVNULL)
        else:
            self.console.print(PromptSite.functional)
    
    def support_open_app(self, filepath: str) -> None:
        """Opens the file depending on the OS. On Linux, it allows you to select an editor."""
        if self.__windows:
            try:
                subprocess.Popen(f'start "" "{filepath}"', shell=True, stderr=subprocess.DEVNULL)
            except PermissionError:
                self.console.print(PromptsHelper.access_error)

        elif self.__darwin:  # macOS
            try:
                subprocess.Popen(["open", filepath], stderr=subprocess.DEVNULL)
            except PermissionError:
                self.console.print(PromptsHelper.access_error)

        elif self.__linux:
            self.console.print(f"\n{PromptsHelper.xdg_open}")
            choice = self.console.input(Prompts.arrows).strip().lower()

            if choice == "y":
                try:
                    subprocess.Popen(["xdg-open", filepath], stderr=subprocess.DEVNULL)
                except subprocess.CalledProcessError:
                    self.console.print(PromptsHelper.not_open)
                except Exception as e:
                    self.console.print(f"Ошибка: {e}")
            else:
                self.__redactor_helper_linux(filepath)

        else:
            self.console.print(PromptSite.functional)

    def __redactor_helper_linux(self, filepath: str) -> None:
        """Allows you to select an editor to open the file manually on Linux."""
        default_editors = ["code", "gedit", "nano", "vim", "nvim", "kate", "micro"]

        self.console.print(f"\n{PromptsHelper.choose}")
        for i, editor in enumerate(default_editors, 1):
            self.console.print(f"{i}. {editor}")
        self.console.print(f"{len(default_editors) + 1}{PromptsHelper.manual}")
        
        choice = self.console.input(Prompts.arrows)

        if not choice.isdigit():
            self.console.print(PromptsHelper.err_number)
            return

        choice = int(choice)

        if 1 <= choice <= len(default_editors):
            editor = default_editors[choice - 1]
        elif choice == len(default_editors) + 1:
            self.console.print(PromptsHelper.redactor_name)
            editor = self.console.input(Prompts.arrows)
        else:
            self.console.print(PromptsMenu.bad_entry)
            return

        if shutil.which(editor) is None:
            self.console.print(f"Редактор '{editor}' не найден в системе")
            return

        try:
            subprocess.Popen([editor, filepath], stderr=subprocess.DEVNULL)
            self.console.print(f"Открываю через '{editor}'")
        except Exception as e:
            self.console.print(f"Не удалось открыть редактор: {e}")

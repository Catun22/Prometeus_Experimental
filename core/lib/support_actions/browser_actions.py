"""
A module that organizes the work of the methods responsible for the functionality of the program for working with links.
"""

from urllib.parse import urlparse

from core.lib.templates.templates import *
from core.lib.prompts.prompts_system import PromptSite


class BrowserActions:
    """A class containing methods for working with the browser and links."""

    def __init__(self) -> None:
        self.__tp = TemplatesHandler()
        self.__hp = self.__tp.hp
        self.__console = self.__tp.console

    def get_link(self, link: str):
        """A method for creating ready-made links to any sites.

        Args:
            link (str): A ready-made link to the website.
        """
        # here we can validate user's input by new method
        new_link = self.__validate_site(link)
        if new_link:
            self.__send_link_for_execution(link)
        else:
            print(f"Неверный ввод ссылки: {link}")

    def open_site(self):
        """The method that opens the page in the browser. User input of the link is required"""
        self.__console.print(PromptSite.link)
        link = self.__console.input(Prompts.arrows)
        # here we can validate user's input by new method
        new_link = self.__validate_site(link)
        if new_link:
            self.__send_link_for_execution(link)
        else:
            print(f"Неверная ссылка: {link}")

    def __send_link_for_execution(self, link: str):
        """Sends the execution link to the subprocess

        Args:
            link (str): Link to execution
        """
        self.__hp.support_page(link)

    def __validate_site(self, link: str) -> bool:
        """Performs a simple validation of the link URL.

        Args:
            link (str): The link to the website.

        Returns:
            bool: Does such a link exist.
        """
        parsed = urlparse(link)
        # for example: https://google.com
        # sheme = https
        # netloc = google.com
        is_url = bool(parsed.scheme and parsed.netloc)
        return is_url

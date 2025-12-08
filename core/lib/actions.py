"""acrions.py

A module that stores the main functions of the entire program.
"""

from core.lib.path_manager import PathManager
from core.lib.prompts.prompts_system import Prompts, PromptsLaw
from core.lib.templates.templates import *
from core.lib.system_apps.findler import findler
from core.lib.support_actions.settings_actions import SettingsActions
from core.lib.support_actions.browser_actions import BrowserActions


class CLI:
    """
    The container class. It contains basic methods that support the "basic" functionality of the entire program.

    Inherit from this class in the "custom" module "actions.py ".

    `templates` is a field that supports the functionality of templates.
    """

    def __init__(self) -> None:
        __pm = PathManager()
        self.menu_path = __pm.menu_path
        self.actions_path = __pm.actions_path

        self.__ba = BrowserActions()
        self.__sa = SettingsActions()
        self.templates = TemplatesHandler()

    ###########################################################
    ###_________________Templates methods___________________###
    ###########################################################
    def create_topic(self) -> None:
        """Creates a template for programming topics (python)"""
        self.templates.create_item(
            cls=Topic, title_prompt=Prompts.theme, path_key="topic"
        )

    def look_topic(self) -> None:
        """Shows a list of created programming templates (python)"""
        self.templates.look_item(cls=Topic, path_key="topic")

    def law_topic(self) -> None:
        """Creates templates on "law" (About the documents)."""
        extra = [
            ("doc_number", PromptsLaw.doc_number),
            ("short_name", PromptsLaw.short_name),
            ("year", PromptsLaw.year),
            ("law_type", PromptsLaw.law_type),
        ]
        self.templates.create_item(
            cls=LawTopic,
            title_prompt=PromptsLaw.doc,
            path_key="law",
            extra_arguments=extra,
        )

    def look_law(self) -> None:
        """Shows a list of created law templates"""
        self.templates.look_item(cls=LawTopic, path_key="law")

    ###########################################################
    ###___________________Browser methods___________________###
    ###########################################################
    def open_page(self) -> None:
        """Opens the page using the entered link."""
        self.__ba.open_site()

    def open_approved_site(self, link: str = "https://google.com") -> None:
        """Opens a pre-prepared link.

        You can inherit from this method and redefine its reference.

        Args:
            link (_type_, optional): A prepared link to a website. Defaults to "https://google.com".
        """
        self.__ba.get_link(link)

    ###########################################################
    ###____________________System methods___________________###
    ###########################################################
    def find_file(self) -> None:
        """Search for files (README) and save by size"""
        findler()

    ###########################################################
    ###_______________Configuration methods_________________###
    ###########################################################
    def _open_menu_settings(self) -> None:
        """
        Opens the settings of the "menu.json" file

        Do not inherit or change.
        """
        self.__sa.menu_settings_handler()

    def _open_config_settings(self) -> None:
        """
        Opens the settings of the "config.json" file.

        Do not inherit or change.
        """
        self.__sa.config_settings_handler()

    def _open_actions_settings(self) -> None:
        """
        Opens the settings of the "actions.json" file.

        Do not inherit or change.
        """
        self.__sa.actions_settings_handler()

    def _open_colors_settings(self) -> None:
        """
        Opens the settings of the "colors.json" file.

        Do not inherit or change.
        """
        self.__sa.colors_settings_handler()

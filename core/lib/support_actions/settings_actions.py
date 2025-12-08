"""
A module containing methods for managing config settings.
"""

from core.lib.templates.templates import *


class SettingsActions:
    """A class containing proxy methods for configs."""

    def __init__(self) -> None:
        self.__tp = TemplatesHandler()
        self.__hp = self.__tp.hp

    def menu_settings_handler(self):
        """
        Opens the settings of the "menu.json" file

        Proxy.
        """
        self.__hp.support_open_app(self.__tp.menu_path)

    def config_settings_handler(self):
        """
        Opens the settings of the "config.json" file.

        Proxy.
        """
        self.__hp.support_open_app(self.__tp.config_path)

    def actions_settings_handler(self):
        """
        Opens the settings of the "actions.json" file.

        Proxy.
        """
        self.__hp.support_open_app(self.__tp.actions_path)

    def colors_settings_handler(self):
        """
        Opens the settings of the "colors.json" file.

        Proxy.
        """
        self.__hp.support_open_app(self.__tp.color_path)

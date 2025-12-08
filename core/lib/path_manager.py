"""
The module responsible for the paths.

"""

import os
import json


class PathManager:
    """
    Manages the application paths.
    1. Searches for configs in user/configs, if not, it takes them from core/configs.
    2. It has default paths for Storage/Topics and Storage/Law.
    3. Loads custom paths from config.json, if any.
    4. Creates directories.
    """

    # If there are no configs in user/configs or in core/configs,
    # it means that the configs in core/configs have been corrupted and the user has not set new configs,
    # therefore default paths are used.
    DEFAULT_PATHS = {
        "topic": os.path.join("Storage", "Topics"),
        "law": os.path.join("Storage", "Law"),
    }

    def __init__(self):
        self.current_file = os.path.abspath(__file__)
        self.base_path = os.path.dirname(
            os.path.dirname(os.path.dirname(self.current_file))
        )

        self.__user_configs_dir = self._get_user_configs_dir()
        self.__core_configs_dir = self._get_core_configs_dir()

        self.menu_path = self._get_config_file_path("menu.json")
        self.actions_path = self._get_config_file_path("actions.json")
        self.color_path = self._get_config_file_path("colors.json")
        self.config_path = self._get_config_file_path("config.json")

        self.config_exists = os.path.exists(self.config_path)

        # Uploading the user's configuration
        self.config = self._load_config()

        # Final paths
        self.paths = self.__final_paths()

        # Creating directories
        self.__ensure_storage_dirs()

    def _get_user_configs_dir(self) -> str:
        """Returns the path to user/configs"""
        return os.path.join(self.base_path, "user", "configs")

    def _get_core_configs_dir(self) -> str:
        """Returns the path to core/configs"""
        return os.path.join(self.base_path, "core", "configs")

    def _get_config_file_path(self, filename: str) -> str:
        """
        Returns the path to the configuration file.

        First it checks user/configs, if not, core/configs.
        """
        user_path = os.path.join(self.__user_configs_dir, filename)
        if os.path.exists(user_path):
            return user_path

        core_path = os.path.join(self.__core_configs_dir, filename)
        if os.path.exists(core_path):
            return core_path

        # If the file is nowhere to be found, return the path to user/configs.
        return user_path

    def _load_config(self) -> dict[str, dict[str, str]]:
        """
        Loads config.json.

        First it checks user/configs, if not, core/configs.
        """
        if not self.config_exists:
            return {"paths": {}}

        try:
            with open(self.config_path, "r", encoding="UTF-8") as f:
                data = json.load(f)
                if "paths" not in data:
                    data["paths"] = {}
                return data
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {"paths": {}}

    def __final_paths(self) -> dict[str, str]:
        """Generates the full paths to the files specified in the config."""
        final: dict[str, str] = {}
        if self.config_exists:
            user_paths = self.config.get("paths", {})
            for key, path in user_paths.items():
                if os.path.isabs(path):
                    final[key] = path
                else:
                    final[key] = os.path.join(self.base_path, path)
        else:
            for key, path in self.DEFAULT_PATHS.items():
                final[key] = os.path.join(self.base_path, path)
        return final

    def __ensure_storage_dirs(self):
        """Creates directories according to the specified paths in the config."""
        for path in self.paths.values():
            os.makedirs(path, exist_ok=True)

    def get_menu_path(self) -> str:
        """Get the path to menu.json"""
        return self.menu_path

    def get_actions_path(self) -> str:
        """Get the path to actions.json"""
        return self.actions_path

    def get_color_path(self) -> str:
        """Get the path to color.json"""
        return self.color_path

    def get_config_path(self) -> str:
        """Get the path to config.json"""
        return self.config_path

    def get_path(self, key: str | None = None):
        """Get all the paths in the config.json"""
        if key:
            return self.paths.get(key)
        return self.paths

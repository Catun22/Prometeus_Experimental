from core.lib.actions import CLI
from user.patterns import *


class MyCLI(CLI):
    def __init__(self) -> None:
        super().__init__()

    def create_library(self):
        self.templates.create_item(
            cls=Library, title_prompt="Введите название: ", path_key="lib"
        )

    def look_library(self):
        self.templates.look_item(cls=Library, path_key="lib")

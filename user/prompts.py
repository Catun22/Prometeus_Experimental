

from core.lib.prompts.prompts_menu import  UserPrompts



class MyUserPrompts(UserPrompts):
    def __init__(self, main_title: str = "Добро пожаловать, господин!", title: str = "Cogito", subtitle: str = "ergo sum") -> None:
        super().__init__(main_title, title, subtitle)
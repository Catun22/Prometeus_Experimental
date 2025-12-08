"""
A module containing a colored panel (title page) of the program.
"""

from rich.text import Text
from rich.panel import Panel
from core.lib.prompts.prompts_system import main_color, second_color, additional_color


class UserPrompts:
    """
    A class containing a colored panel.

    When inheriting, it allows you to change the test panel, but not its color.
    
    To change the color, change the settings of the "colors.json".
    """

    def __init__(self, main_title: str = "Добро пожаловать, господин!", title: str = "Cogito", subtitle: str = "ergo sum", to_do: str = "Чем вы займетесь сегодня?") -> None:
        
        self.welcome = Panel.fit(
            f"[bold]{main_title}[/bold]",
            style=main_color,
            border_style=second_color,
            title=f"[bold italic]{title}[/bold italic]",
            title_align="left",
            subtitle=f"[bold italic]{subtitle}[/bold italic]",
            subtitle_align="right"
        )

        self.choise = Text(f"{to_do}", style=additional_color)
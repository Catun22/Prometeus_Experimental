"""
A module that displays errors to the user.

"""

from rich.console import Console
from rich.panel import Panel


console = Console()


def error_print(message: object) -> None:
    """A container that displays any errors using methods from the "rich" library.

    Args:
        message (object): The error object. For example, AttributeError.
    """
    console.print()
    console.print(
        Panel.fit(
            f"[bold red]{message}[/bold red]",
            border_style="bold yellow",
            title="Configuration error",
            title_align="left",
            subtitle="Correct the code in configs/actions.json",
            subtitle_align="right",
        )
    )
    console.print()

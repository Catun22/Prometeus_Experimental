"""
Contains colored prompta for `print` and `input'.

"""


from rich.text import Text
from core.utilits.opener_json import open_json


from core.lib.path_manager import PathManager as pm

path = pm()

class Default:

    colour_1: str
    colour_2 : str
    colour_3 : str
    colour_4 : str
    colour_5 : str

colors: dict[str, str] = open_json(path.get_color_path())

for key, value in colors.items():
    setattr(Default, key, value)

main_color = Default.colour_1 + " bold"
second_color = Default.colour_2 + " bold"
third_color = Default.colour_3 + " bold"
additional_color = Default.colour_4 + " bold"
support_color = Default.colour_5 + " bold"


class Prompts:
   
    arrows = Text(">>> ", style=f"{third_color} blink")
    theme = Text("Введите название: ", style=main_color)
    author = Text("Введите имя автора: ", style=main_color)
    save = Text("\nПример сохранения: ", style=main_color)
    file_name = Text("название_темы_topic.md", style=support_color)
    save_path = Text("\nВведите путь сохранения или нажмите ", style=main_color)
    enter = Text("Enter", style=additional_color)
    default = Text("для установки по умолчанию", style=main_color)
    file_saved = Text("Файл сохранен: ", style=main_color)
    tags = Text('Введите теги. "Пустой ввод" - завершить.', style=main_color)


class PromptsLaw:
    doc = Text("Введите название темы или документа.", style=main_color)
    doc_number = Text(
        'Введите номер документа или "пустой ввод", если нет.', style=main_color
    )
    short_name = Text(
        'Введите короткое название документа или "пустой ввод", если нет.',
        style=main_color,
    )
    year = Text(
        'Введите год принятия документа или "пустой ввод", если нет.', style=main_color
    )
    law_type = Text(
        'Введите область права или "пустой ввод", если нет.', style=main_color
    )


class PromptsMenu:
    bad_entry = Text("Неверный ввод, попробуйте снова.", style=third_color)
    main_menu = Text("Вы в главном меню", style=main_color)
    exit = Text("[q] - выход", style=third_color)
    back = Text("[b] - назад", style=third_color)
    perform_action = Text("Выполняем действие: ", style=main_color)


class PromptSite:
    link = Text("Введите ссылку", style=main_color)
    functional = Text(
        "Полный фунционал программы поддерживается только на: Linux, macOS, Windows.",
        style=third_color,
    )


class PromptsHelper:
    access_error = Text("Ошибка доступа при открытии файла", style=third_color)
    xdg_open = Text("Открыть через системное приложение (xdg-open)?[Y/n]", style=main_color)
    not_open = Text("Не удалось открыть через xdg-open, используйте редактор", style=third_color)
    choose = Text("Выберите редактор:", style=main_color)
    manual = Text(". Ввести свой вручную", style=main_color)
    err_number = Text("Ошибка: введите число", style=third_color)
    redactor_name = Text("Введите имя или полный путь редактора: ", style=main_color)

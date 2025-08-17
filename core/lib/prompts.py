"""prompts.py

Содержит раскрашенные промпты для `print` и `input`.
"""

from core.ANSI.ANSI import FG, EFFECT, FG_BRIGHT


class Prompts:
    """Содержит покрашенные промпты для текста.
    """
    arrows = ">>> " + FG.red + EFFECT.bold
    theme = "Введите название:" + FG.green + EFFECT.bold
    save = "\nПример сохранения:" + FG.green + EFFECT.bold
    file_name = "название_темы_topic.md" + FG.white + EFFECT.bold
    save_path = "\nВведите путь сохранения или нажмите" + FG.green + EFFECT.bold
    enter = "Enter" + FG.blue + EFFECT.bold
    default = "для установки по умолчанию" + FG.green + EFFECT.bold
    file_saved = "Файл сохранен:" + FG.green + EFFECT.bold

    # Отдельное приветствие
    welcome = "Добро пожаловать, господин!" + FG.green + EFFECT.underline + EFFECT.bold


class MenuPrompts:
    """Содержит покрашенные промпты для текста в меню.
    """
    choise = "Чем вы займетесь сегодня?" + FG.green + EFFECT.bold
    bad_entry = "Неверный ввод, попробуйте снова." + FG_BRIGHT.red + EFFECT.bold
    main_menu = "Вы в главном меню" + FG.green + EFFECT.bold
    exit = "Выход" + FG.red + EFFECT.bold
    back = "Назад" + FG.blue + EFFECT.bold
    perform_action = "Выполняем действие:" + FG.green + EFFECT.bold

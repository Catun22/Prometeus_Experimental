"""prompts.py

Содержит раскрашенные промпты для `print` и `input`.

"""

from rich.text import Text
from rich.panel import Panel


class Default:
    default_theme_green = "#00B74A" + " bold"
    default_theme_yellow = "#FFCF00" + " bold"
    default_theme_red = "#FF3100" + " bold"
    default_theme_blue = "#3415B0" + " bold"
    white = "#FFFFFF" + " bold"


main_color = Default.default_theme_green
second_color = Default.default_theme_yellow
third_color = Default.default_theme_red
additional_color = Default.default_theme_blue
support_color = Default.white  # Цвет для  цифр и прочего текста


class Prompts:
    """Содержит покрашенные промпты для текста."""

    # Отдельное приветствие
    welcome = Panel.fit(
        "[bold]Добро пожаловать, господин![/bold]",
        style=main_color,
        border_style=second_color,
        title="[bold italic]Cogito[/bold italic]",
        title_align="left",
        subtitle="[bold italic]ergo sum[/bold italic]",
        subtitle_align="right",
    )

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
    choise = Text("Чем вы займетесь сегодня?", style=additional_color)
    bad_entry = Text("Неверный ввод, попробуйте снова.", style=third_color)
    main_menu = Text("Вы в главном меню", style=main_color)
    exit = Text("Выход", style=third_color)
    back = Text("Назад", style=third_color)
    perform_action = Text("Выполняем действие: ", style=main_color)


class PromptsDict:
    """Содержит покрашенные промпты для словаря (через Rich Text)."""

    mode_interactive = Panel.fit(
        "ИНТЕРАКТИВНЫЙ СЛОВАРЬ",
        style=main_color,
        border_style=second_color,
        title="[bold italic]English-Français[/bold italic]",
        title_align="left",
        subtitle="[bold italic]Deutsch-Español[/bold italic]",
        subtitle_align="right",
    )
    loaded_words = Text("Загружено слов: ", style=main_color)
    equal = Text("=" * 50, style=third_color)

    add_word = Text("Добавить слово", style=main_color)
    find_word = Text("Найти слово", style=main_color)
    edit_word = Text("Редактировать слово", style=main_color)
    delete_word = Text("Удалить слово", style=third_color)
    show_word = Text("Показать список слов", style=main_color)
    save_word = Text("Сохранить словарь", style=main_color)
    exit_word = Text("Выйти", style=third_color)
    choose_word = Text("Выберите действие (1-7)", style=main_color)

    enter_word = Text("Введите слово: ", style=main_color)
    word_no_space = Text("Слово не может быть пустым.", style=third_color)

    __stop = Text("стоп", style=third_color)

    enter_language = (
        Text(
            "Введите язык перевода:\n"
            "\n"
            "English [en] - английский\n"
            "Deutsch [ge] - немецкий\n"
            "Français [fr] - французский\n"
            "Español [es] - испанский\n"
            "\n"
            "Для завершения введите: стоп",
            style=main_color,
        )
        + Text("Для завершения введите: '")
        + __stop
        + Text("'")
    )

    enter_translate = Text("Введите перевод: ", style=main_color)
    enter_transcript = Text("Введите транскрипцию (если есть): ", style=main_color)
    enter_context = Text(
        "Введите контекст (или стоп для завершения): ", style=main_color
    )

    enter_word_to_find = Text("Введите слово для поиска: ", style=main_color)
    ask_no_space = Text("Поисковый запрос не может быть пустым.", style=third_color)
    exactly_find = Text("Точное совпадение:", style=main_color)
    count = Text("Найдено совпадений:", style=main_color)
    look_or_back = Text(
        "Введите номер для просмотра (или 0 для возврата):", style=main_color
    )
    no_matches = Text("Совпадений не найдено.", style=third_color)

    enter_to_edit = Text("Введите слово для редактирования:", style=main_color)
    not_found_in_dict = Text("Слово не найдено в словаре.", style=third_color)

    current_data = Text("Текущие данные:", style=main_color)
    want_to_change = Text("Что вы хотите изменить?", style=main_color)
    edit_base_word = Text("Изменить базовое слово", style=second_color)
    edit_translate = Text("Добавить/изменить перевод", style=main_color)
    edit_transcript = Text("Добавить/изменить транскрипцию", style=main_color)
    edit_context = Text("Добавить контекст", style=main_color)
    delete_context = Text("Удалить контекст", style=third_color)

    choose_action = Text("Выберите действие (1-5):", style=main_color)

    new_base = Text("Введите новое базовое слово:", style=main_color)
    new_language = Text(
        "Введите язык:\n"
        "English [en] - английский\n"
        "Deutsch [ge] - немецкий\n"
        "Français [fr] - французский\n"
        "Español [es] - испанский",
        style=main_color,
    )
    new_enter_transcript = Text("Введите транскрипцию:", style=main_color)
    new_enter_context = Text("Введите контекст:", style=main_color)
    current_context = Text("Текущие контексты:", style=main_color)
    number_context_delete = Text(
        "Введите номер контекста для удаления:", style=third_color
    )
    word_to_delete = Text("Введите слово для удаления:", style=third_color)

    page = Text("Страница", style=main_color)
    all_words = Text("всего слов:", style=main_color)

    save_edits = Text("Сохранить изменения перед выходом? (д/н):", style=main_color)
    wrong_choose = Text("Неверный выбор. Попробуйте снова.", style=main_color)

    saved_dict = Text("Словарь сохранен в файл:", style=main_color)

    word = Text("Слово", style=main_color)
    added = Text("добавлено в словарь.", style=main_color)
    already_have = Text("уже есть в словаре.", style=second_color)
    deleted = Text("удалено из словаря.", style=third_color)
    no_found = Text("не найдено в словаре.", style=second_color)
    exists = Text("уже существует в словаре.", style=third_color)
    edited = Text("успешно изменено.", style=main_color)

    must_be_str = Text("Ошибка: new_base должен быть строкой", style=third_color)
    no_file_save = Text("Не указан файл для сохранения.", style=third_color)

    next_page = Text("- следующая страница", style=main_color)
    back_page = Text("- предыдущая страница", style=main_color)
    exit_page = Text("- выход", style=main_color)


class PromptSite:
    link = Text("Введите ссылку", style=main_color)
    functional = Text(
        "Полный фунционал программы поддерживается только на: Linux, macOS, Windows.",
        style=third_color,
    )


class Errors:
    error_steam = Text("Steam не найден на вашей системе", style=third_color)

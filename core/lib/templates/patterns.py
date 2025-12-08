"""

It contains basic template classes, the text of which will be inserted into a file with the `.md` extension.
"""

import os
from datetime import date
from core.lib.prompts.prompts_system import Prompts


class TemplateMd:
    def __init__(
        self,
        *,
        title: str = "Название титульника",
        tags: list[str] | None = None,
        emoticon: str = "📝",
        suffix: str = "",
    ) -> None:

        self.__title = title  # It is possible to check for "valid" characters, but I did not do this.
        self.__tags = tags or []
        self.__emoticon = emoticon
        self.__date = date.today()

        self.__file_name = self.__title.lower().replace(" ", "_") + suffix
        self.__path_to_file = ""
        self.__dir_path: str | None = None

        self.__content = ""
        self.structure()

    def structure(self) -> None:
        """
        The main method that stores the structure/framework/skeleton of the template

        When creating a new template class, you must inherit from this method.

        For example, as follows:
        ```
        class MyTemplate:
            def _structure(self) -> None:
                super()._structure()
        ```

        This method is a container.
        """
        # The title of the topic with a smiley face and the date of creation
        self.__content += f"# {self.__emoticon} {self.__title}\n\n"
        self.__content += f"#### Дата создания: {self.__date}\n\n"

        if self.__tags:
            self.add_section(
                "🏷️ Теги", [f"Теги: #{' #'.join(sorted(set(self.__tags)))}"]
            )

    def add_section(self, title: str, items: list[str]) -> None:
        """Adds a section with a list of items"""
        self.__content += f"## {title}\n\n"  # Title page of the section
        for item in items:  # If there is a list with "subsections"
            # Then we put "-", a space and the name of the item from the list
            self.__content += f"- {item}\n"
        self.__content += "\n"  # Adding an empty line at the end

    def add_code_section(self, title: str, code: str) -> None:
        """Adds a section with a block of code"""
        self.__content += f"## {title}\n\n"
        self.__content += f"```python\n{code}\n```\n\n"  # Making a block with the code; python so that .md knows that the code is in this language

    def __path(self, path: str | None = None) -> None:
        """Creates paths"""
        if self.__path_to_file:  # the path has already been set via set_default_path
            return
        if (
            path is None
        ):  # If the path is not specified, it will be created next to it in lowercase:
            self.__path_to_file = self.get_file_name()
            self.__dir_path = os.getcwd()
            return

            # If the path is specified
            # If the path ends with the extension (that is, you entered the path to the file, not the directory)
        if path.endswith(".md"):
            self.__path_to_file = path
            # Then the path to the folder (with the file) will be like this:
            self.__dir_path = os.path.dirname(self.__path_to_file)
            if self.__dir_path:  # If there is something in the __dir_path
                # Then we will create directories along this path (if we enter a new path)
                os.makedirs(self.__dir_path, exist_ok=True)

        else:
            # If we didn't write the extension (that is, we didn't write the file path)
            # Then we create directories along the way
            os.makedirs(path, exist_ok=True)
            # The file name will be like this:
            self.__file_name = self.__title.lower().replace(" ", "_")
            # And the file path is: directory path + file name
            self.__path_to_file = os.path.join(path, self.get_file_name())
            self.__dir_path = path

    def __save(self, path: str) -> None:
        """Writes it to a file"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.__content)
        print(Prompts.file_saved, os.path.abspath(path))

    def get_available_files(
        self, directory: str | None = None, end: str = ".md"
    ) -> list[str]:
        """Returns a list .md files in the specified directory"""
        directory = directory or os.getcwd()
        try:
            return [f for f in os.listdir(directory) if f.endswith(end)]
        except FileNotFoundError:
            print(f"Директория {directory} не найдена.")
            return []
        except PermissionError:
            print(f"Нет доступа к директории {directory}.")
        return []

    def set_default_path(self, path: str) -> None:
        """
        Sets the default path.
        If a file (.md) is specified, we take it.
        If a folder is specified, we save the file with the theme name there.
        """
        if path.endswith(".md"):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            self.__path_to_file = path
            self.__dir_path = os.path.dirname(path)
        else:
            os.makedirs(path, exist_ok=True)
            self.__path_to_file = os.path.join(path, self.get_file_name())
            self.__dir_path = path

    def get_path(self) -> str:
        """Get the full file path"""
        return self.__path_to_file

    def get_dir_path(self) -> str | None:
        """The full path to the directory"""
        return os.path.abspath(self.__dir_path) if self.__dir_path else None

    def get_file_name(self) -> str:
        """Get the file name"""
        if self.__file_name.endswith(".md"):
            return str(self.__file_name)
        return f"{self.__file_name}.md"

    def start(self, path: str | None = None) -> None:
        """Launch"""
        self.__path(path)
        # After the whole procedure, we save
        self.__save(self.get_path())


class Topic(TemplateMd):
    """Creates a template for programming topics (python)"""

    def __init__(
        self,
        title: str = "Название темы",
        emoticon: str = "🐍",
        tags: list[str] | None = None,
    ) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_topic", tags=tags)

    def get_available_files(
        self, directory: str | None = None, end: str = "_topic.md"
    ) -> list[str]:
        return super().get_available_files(directory, end)

    def structure(self) -> None:
        super().structure()
        self.add_section(
            "😸 Общее представление",
            [
                "Что это?",
                "Для чего используется?",
                "Где применяется?",
                "Почему нужно знать?",
            ],
        )

        self.add_section(
            "😺 Понятия и термины", ["Термин 1 — определение", "Термин 2 — определение"]
        )

        # A block for adding code according to a template
        self.add_code_section(
            "😼 Структура & Синтаксис",
            '# Пример кода\nwith open(\'file.txt\', "w", encoding="utf-8") as f:\n    data = f.write()',
        )

        self.add_section(
            "😾 Примеры использования",
            ["Простой пример", "Сложный пример", "Практический пример"],
        )

        self.add_section(
            "🐯 Практика", ["Что стоит попробовать руками, чтобы закрепить?"]
        )

        self.add_section(
            "😡 Подводные камни и ошибки",
            [
                "Что часто путается?",
                "Где находятся частые ошибки?",
                "Что нужно помнить?",
            ],
        )

        self.add_section(
            "🧐 Сравнение & аналоги", ["try/finally vs with", "генераторы vs итераторы"]
        )

        self.add_section(
            "😶 Связанные темы",
            ["Указать смежные темы: классы, итераторы, файловая система"],
        )

        self.add_section(
            "🤓 Полезные ссылки и документация",
            [
                "Документация Python",
                "PEP 343 — The 'with' Statement",
                "Видео, статьи, конспекты",
            ],
        )

        self.add_section("😤 Итоги", ["Краткое резюме", "3–5 главных выводов"])


class LawTopic(TemplateMd):
    """Creates a template for topics by right with the ability to specify additional identifiers"""

    def __init__(
        self,
        title: str = "Название темы/документа",
        doc_number: str | None = None,
        year: str | None = None,
        law_type: str | None = None,
        short_name: str | None = None,
        tags: list[str] | None = None,
        emoticon: str = "⚖️",
    ) -> None:

        self.__doc_number = doc_number
        self.__year = year
        self.__law_type = law_type
        self.__short_name = short_name
        super().__init__(title=title, emoticon=emoticon, suffix="_law", tags=tags)

    def get_available_files(
        self, directory: str | None = None, end: str = "_law.md"
    ) -> list[str]:
        return super().get_available_files(directory, end)

    def structure(self) -> None:
        super().structure()
        # That's how you can do it too.
        # Create a list right in the class and drop it into the section
        general_info: list[str] = []
        if self.__short_name:
            general_info.append("Короткое название: " + self.__short_name)
        if self.__doc_number:
            general_info.append("Номер документа: " + self.__doc_number)
        if self.__year:
            general_info.append("Год принятия: " + self.__year)
        if self.__law_type:
            general_info.append("Область права: " + self.__law_type)

        self.add_section("😸 Общая информация", general_info)

        self.add_section(
            "😺 Понятия и термины", ["Термин 1 — определение", "Термин 2 — определение"]
        )

        self.add_section(
            "📃Структура документа",
            [
                "Основные статьи и разделы",
                "Ключевые нормы и положения",
                "Примечания и ссылки на смежные статьи/акты",
            ],
        )

        self.add_section(
            "😾 Примеры",
            [
                "Пример из практики",
                "Применение нормы на реальном примере",
            ],
        )

        self.add_section(
            "🔍 Практический анализ",
            ["Разбор спорных моментов", "Комментарии и выводы"],
        )

        self.add_section(
            "😡 Подводные камни и ошибки",
            ["Частые ошибки при толковании", "Особенности применения нормы"],
        )

        self.add_section("😤 Итоги", ["Краткое резюме документа", "Главные выводы"])

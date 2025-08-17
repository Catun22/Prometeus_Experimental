"""pattern.py

Содержит основные классы-шаблоны, текст которых вставится в файл `.md.`
"""

from typing import Optional
import os
from datetime import date
from core.lib.prompts import Prompts


class __TemplateMd:  # Создадим базовый класс
    def __init__(
        self, title: str = "Название титульника", emoticon: str = "📝", suffix: str = ""
    ) -> None:  # Ставим название темы по умолчанию, если ввода не будет
        
        self.__title = title  # Можно провести проверку на "допустимые" символы
        self.__emoticon = emoticon
        self.__date = date.today()
        
        self.__file_name = self.__title.lower().replace(" ", "_") + suffix
        self.__path_to_file = ""
        self.__dir_path: Optional[str] = None

        self.__content = ""  # Пустое поле
        self._structure()  # Вызываем метод (главный)

    def _structure(self) -> None:
        """
        Основной метод, хранящий структуру/каркас/скелет шаблона
        
        При создании нового класса-шаблона, необходимо наследоваться от этого метода.

        Например, следующим образом:
        ```
        class MyTemplate:
            def _structure(self) -> None:
                super()._structure()
        ```

        Этот метод - контейнер.
        """
        # Заголовок темы со смайликом и датой создания
        self.__content += f"# {self.__emoticon} {self.__title}\n\n"
        self.__content += f"#### Дата создания: {self.__date}\n\n"

    def _add_section(self, title: str, items: list[str]) -> None:
        """Добавляет раздел со списком элементов"""
        self.__content += f"## {title}\n\n"  # Титульник раздела
        for item in items:  # Если есть список с "подразделами"
              # То ставим "-", пробел и имя элемента из списка
            self.__content += f"- {item}\n"
        self.__content += "\n"  # Добавляем пустую строку в конце

    def _add_code_section(self, title: str, code: str) -> None:
        """Добавляет раздел с блоком кода"""
        self.__content += f"## {title}\n\n"  #  Титульник, как и в предыдущем методе
        self.__content += f"```python\n{code}\n```\n\n"  # Делаем блок с кодом; python чтобы .md знал что код на этом языке


    def __path(self, path: Optional[str] = None) -> None:  # Запуск и сохранение
        """Создает пути"""
        if self.__path_to_file:  # путь уже установлен через set_default_path
            return
        if path is None:  # Если путь не указан, то создадится рядом в нижнем регистре:
            self.__path_to_file = self.get_file_name()
            self.__dir_path = os.getcwd()
        else: 
            # Если путь указан
            # Если путь заканчивается на расширение (то есть ввели путь к файлу, а не директории)
            if path.endswith(".md"):
                self.__path_to_file = path  # Путь к файлу будет равен пути
                # Тогда путь к папке (с файлом) будет таким:
                self.__dir_path = os.path.dirname(self.__path_to_file)
                if self.__dir_path:  # Если в __dir_path что-то будет
                    # То создадим директории по этому пути (если мы вводим новый путь)
                    os.makedirs(self.__dir_path, exist_ok=True)

            else: 
                # Если мы не писали расширение (то есть не писали путь с файлом)
                # То создаем директории по пути
                os.makedirs(path, exist_ok=True)
                # Имя файла будет таким:
                self.__file_name = self.__title.lower().replace(' ', '_')
                # А путь к файлу: путь к директории + имя файла
                self.__path_to_file = os.path.join(path, self.get_file_name())  
                self.__dir_path = path

    def __save(self, path: str) -> None:
        """Записывает в файл"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.__content)
        print(Prompts.file_saved, os.path.abspath(path))

    def set_default_path(self, path: str) -> None:
        """
        Устанавливает путь по умолчанию.
        Если указан файл (.md) — берём его.
        Если указана папка — сохраняем туда файл с названием темы.
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
        """Получить полный путь к файлу"""
        return self.__path_to_file
    
    def get_dir_path(self) -> Optional[str]:
        return os.path.abspath(self.__dir_path) if self.__dir_path else None
    
    def get_file_name(self) -> str:
        """Получить имя файла"""
        if self.__file_name.endswith(".md"):
            return str(self.__file_name)
        return f"{self.__file_name}.md"

    def start(self, path: Optional[str] = None) -> None:
        """Запуск"""
        self.__path(path)
        # После всей процедуры сохраняем
        self.__save(self.get_path())


class Topic(__TemplateMd):
    """Создает шаблон для тем по программированию (python)"""

    def __init__(self, title: str = "Название темы", emoticon: str = "🐍") -> None:
        super().__init__(title, emoticon, suffix="_topic")

    def _structure(self) -> None:
        super()._structure()
        # Основные разделы. Инкапсулируем
        self._add_section(
            "😸 Общее представление",
            [
                "Что это?",
                "Для чего используется?",
                "Где применяется?",
                "Почему нужно знать?",
            ],
        )

        self._add_section(
            "😺 Понятия и термины", ["Термин 1 — определение", "Термин 2 — определение"]
        )

        # Блок для добавления кода по шаблону
        self._add_code_section(
            "😼 Структура & Синтаксис",
            '# Пример кода\nwith open(\'file.txt\', "w", encoding="utf-8") as f:\n    data = f.read()',
        )

        self._add_section(
            "😾 Примеры использования",
            ["Простой пример", "Сложный пример", "Практический пример"],
        )

        self._add_section(
            "🐯 Практика", ["Что стоит попробовать руками, чтобы закрепить?"]
        )

        self._add_section(
            "😡 Подводные камни и ошибки",
            [
                "Что часто путается?",
                "Где находятся частые ошибки?",
                "Что нужно помнить?",
            ],
        )

        self._add_section(
            "🧐 Сравнение & аналоги", ["try/finally vs with", "генераторы vs итераторы"]
        )

        self._add_section(
            "😶 Связанные темы",
            ["Указать смежные темы: классы, итераторы, файловая система"],
        )

        self._add_section(
            "🤓 Полезные ссылки и документация",
            [
                "Документация Python",
                "PEP 343 — The 'with' Statement",
                "Видео, статьи, конспекты",
            ],
        )

        self._add_section("😤 Итоги", ["Краткое резюме", "3–5 главных выводов"])


class Library(__TemplateMd):
    """Создает шаблон для библиотек по программированию (python)"""

    def __init__(self, title: str = "Название библиотеки", emoticon: str = "🐍") -> None:
        super().__init__(title, emoticon, suffix="_library")

        self._add_section(
            "😸 ГЛАВА 1. ОБЩЕЕ ПРЕДСТАВЛЕНИЕ БИБИОТЕКИ",
            [
                "**Описание библиотеки:**",
                "**Альтернативы библиотеки и сравнение:**"
            ]
        )
        
        self._add_section(
            "😺 ГЛАВА 2. УСТАНОВКА И НАСТРОЙКА",
            [
                "**Установка:**",
                "**Проверка работоспособности:**",
                "**Ссылки на документацию:**"
            ]
        )
        
        self._add_section(
            "😼 ГЛАВА 3. БАЗОВОЕ ИСПОЛЬЗОВАНИЕ БИБЛИОТЕКИ",
            [
                "**Простейший пример:**",
                "**Ключевые объекты, классы, функции:**",
                "**Основные методы и атрибуты:**"
            ]
        )
        
        self._add_section(
            "😾 ГЛАВА 4. ПРАКТИЧЕСКОЕ ПРИМЕНЕНИЕ БИБИОТЕКИ",
            [
                "**Практический пример:**",
                "**Своё практическое применение:**"
            ]
        )
        
        self._add_section(
            "😽 ГЛАВА 5. РАЗБОР СЛОЖНЫХ МОМЕНТОВ",
            [
                "**Ошибки:**",
                "**Логика изнутри:**",
                "**Как расширяется:**"
            ]
        )
        
        self._add_section(
            "😿 ГЛАВА 6. ПРОЕКТ И ПРАКТИКА",
            [
                "**Свой проект:**",
                "**Упаковка в шаблон:**"
            ]
        )
        
        self._add_section(
            "🙀 ГЛАВА 7. ДОКУМЕНТАЦИЯ И ЗАКРЕПЛЕНИЕ",
            [
                "**Обзор официальной документации:**",
                "**Закладки с полезными ссылками:**",
                "**Личный конспект:**"
            ]
        )
        
        self._add_section(
            "😻 ГЛАВА 8. ИТОГ",
            [
                "**Понятно:**",
                "**Не понятно:**",
                "**Что дальше:**"
            ]
        )

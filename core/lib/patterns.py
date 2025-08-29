"""pattern.py

Содержит основные классы-шаблоны, текст которых вставится в файл `.md.`
"""
import os
from typing import Optional
from datetime import date

from core.lib.prompts import Prompts


class TemplateMd:  # Создадим базовый класс
    def __init__(
        self, *, title: str = "Название титульника", tags: Optional[list[str]] = None, emoticon: str = "📝", suffix: str = ""
    ) -> None:  # Ставим название темы по умолчанию, если ввода не будет
        
        self.__title = title  # Можно провести проверку на "допустимые" символы
        self.__tags = tags or []
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

        if self.__tags:
            self._add_section(
                "🏷️ Теги",
                [f"Теги: #{' #'.join(sorted(set(self.__tags)))}"]
            )

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
            return
        
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

    def get_available_files(self, directory: Optional[str] = None, end: str =".md") -> list[str]:
        """Возвращает список .md файлов в указанной директории"""
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


class Topic(TemplateMd):
    """Создает шаблон для тем по программированию (python)"""

    def __init__(self, title: str = "Название темы", emoticon: str = "🐍", tags: Optional[list[str]] = None) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_topic", tags=tags)

    def get_available_files(self, directory: Optional[str] = None, end: str = "_topic.md") -> list[str]:
        return super().get_available_files(directory, end)

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
            '# Пример кода\nwith open(\'file.txt\', "w", encoding="utf-8") as f:\n    data = f.write()',
        )

        self._add_section("😾 Примеры использования", ["Простой пример", "Сложный пример", "Практический пример"])

        self._add_section(
            "🐯 Практика", ["Что стоит попробовать руками, чтобы закрепить?"]
        )

        self._add_section(
            "😡 Подводные камни и ошибки",
            [
                "Что часто путается?",
                "Где находятся частые ошибки?",
                "Что нужно помнить?"
            ]
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


class Library(TemplateMd):
    """Создает шаблон для библиотек по программированию (python)"""

    def __init__(self, title: str = "Название библиотеки", emoticon: str = "🐍", tags: Optional[list[str]] = None) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_library", tags=tags)

    def get_available_files(self, directory: Optional[str] = None, end: str = "_library.md") -> list[str]:
        return super().get_available_files(directory, end)
    
    def _structure(self) -> None:
        super()._structure()
        self._add_section(
            "😸 ГЛАВА 1. ОБЩЕЕ ПРЕДСТАВЛЕНИЕ БИБЛИОТЕКИ",
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


class HTMLTopic(TemplateMd):
    """Создает шаблон для тем по HTML"""

    def __init__(self, title: str = "Название темы", emoticon: str = "🌐", tags: Optional[list[str]] = None) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_html", tags=tags)

    def get_available_files(self, directory: Optional[str] = None, end: str = "_html.md") -> list[str]:
        return super().get_available_files(directory, end)

    def _structure(self) -> None:
        super()._structure()

        self._add_section(
            "😸 Общее представление",
            [
                "Что это за тег/структура?",
                "Для чего используется в HTML?",
                "Где применяется чаще всего?",
                "Почему важно знать?",
            ],
        )

        self._add_section(
            "😺 Понятия и термины",
            [
                "Термин 1 — определение",
                "Термин 1 — определение",
            ],
        )
    
        self._add_code_section(
            "😼 Структура & Синтаксис",
            "<!-- Пример кода -->\n<p>Пример абзаца</p>\n<a href='https://example.com'>Ссылка</a>",
        )

    
        self._add_section(
            "😾 Примеры использования",
            ["Простой пример", "Сложный пример", "Практический пример"],
        )

    
        self._add_section(
            "🐯 Практика",
            ["Что стоит попробовать руками, чтобы закрепить?"],
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
            "🧐 Сравнение & аналоги",
            ["div vs section", "span vs strong", "form vs fieldset"],
        )


        self._add_section(
            "😶 Связанные темы",
            ["Указать смежные темы"],
        )

        self._add_section(
            "🤓 Полезные ссылки и документация",
            [
                "HTML Documentation"
            ],
        )

        self._add_section(
            "😤 Итоги",
            ["Краткое резюме", "3–5 главных выводов"],
        )

        
class CssTopic(TemplateMd):
    """Создает шаблон для тем по CSS"""

    def __init__(self, title: str = "Название темы", emoticon: str = "🎨", tags: Optional[list[str]] = None) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_css", tags=tags)

    def get_available_files(self, directory: Optional[str] = None, end: str = "_css.md") -> list[str]:
        return super().get_available_files(directory, end)

    def _structure(self) -> None:
        super()._structure()

        self._add_section(
            "😸 Общее представление",
            [
                "Что это?",
                "Для чего используется?",
                "Где применяется?",
                "Почему нужно знать?",
            ]
        )

        self._add_section(
            "😺 Понятия и термины", ["Термин 1 — определение", "Термин 2 — определение"])

        self._add_code_section(
            "😼 Структура & Синтаксис",
            "/* Пример кода */\nbody {\n    background-color: #f0f0f0;\n    font-family: Arial, sans-serif;\n}\n\na:hover {\n    color: red;\n}",
        )
 
        self._add_section(
            "😾 Примеры использования",
            [
               "Простой пример", "Сложный пример", "Практический пример"
            ]
        )
        self._add_section(
            "🐯 Практика",
            [
                "Что стоит попробовать руками, чтобы закрепить?"
            ]
        )

        self._add_section(
            "😡 Подводные камни и ошибки",
            [
                "Что часто путается?",
                "Где находятся частые ошибки?",
                "Что нужно помнить?"
            ]
        )

        self._add_section(
            "🧐 Сравнение & аналоги",
            [
                "inline vs block vs inline-block",
                "absolute vs relative vs fixed vs sticky",
                "Flexbox vs Grid",
            ]
        )

        self._add_section(
            "😶 Связанные темы",
            [
                "Указать смежные темы"
            ]
        )

        self._add_section(
            "🤓 Полезные ссылки и документация",
            [
                "CSS Documentation"
            ]
        )

        self._add_section(
            "😤 Итоги",
            [
               "Краткое резюме", "3–5 главных выводов"
            ]
        )


class JsTopic(TemplateMd):
    """Создает шаблон для тем по JavaScript"""

    def __init__(self, title: str = "Название темы", emoticon: str = "⚡", tags: Optional[list[str]] = None) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_js", tags=tags)

    def get_available_files(self, directory: Optional[str] = None, end: str = "_js.md") -> list[str]:
        return super().get_available_files(directory, end)

    def _structure(self) -> None:
        super()._structure()

        self._add_section(
            "😸 Общее представление",
            [
                "Что это?",
                "Для чего используется?",
                "Где применяется?",
                "Почему нужно знать?"
            ]
        )

        self._add_section(
            "😺 Понятия и термины",
            [
               "Термин 1 — определение", "Термин 2 — определение"
            ]
        )
        self._add_code_section(
            "😼 Структура & Синтаксис",
            "// Пример кода\nlet name = 'Господин';\nfunction greet() {\n    console.log(`Привет, ${name}!`);\n}\ngreet();",
        )

        self._add_section(
            "😾 Примеры использования",
            [
                "Простой пример", "Сложный пример", "Практический пример"
            ]
        )
        self._add_section(
            "🐯 Практика",
            [
                "Что стоит попробовать руками, чтобы закрепить?"
            ]
        )
        self._add_section(
            "😡 Подводные камни и ошибки",
            [
                "Что часто путается?",
                "Где находятся частые ошибки?",
                "Что нужно помнить?"
            ]
        )

        self._add_section(
            "🧐 Сравнение & аналоги",
            [
                "function vs arrow function",
                "var vs let vs const",
                "for vs forEach vs map",
                "События через addEventListener vs onclick",
            ],
        )

        self._add_section(
            "😶 Связанные темы",
            [
              "Указать смежные темы"
            ]
        )

        self._add_section(
            "🤓 Полезные ссылки и документация",
            [
                "JavaScript Documentation",
            ]
        )

        self._add_section(
            "😤 Итоги",
            [
                "Краткое резюме", "3–5 главных выводов"
            ]
        )


class EnglishTemplate(TemplateMd):
    """Template for studying English topics"""

    def __init__(self, title: str = "English Topic", emoticon: str = "🇬🇧", tags: Optional[list[str]] = None) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_english", tags=tags)

    def get_available_files(self, directory: Optional[str] = None, end: str = "_english.md") -> list[str]:
        return super().get_available_files(directory, end)

    def _structure(self) -> None:
        super()._structure()
        self._add_section(
            "📖 Introduction",
            ["What is the topic?", "Where is it used?", "Why is it important?"]
        )
        self._add_section(
            "🔑 Rules & Structure",
            ["Main rule", "Exceptions", "Useful tables/charts"]
        )
        self._add_section(
            "📝 Examples",
            ["Simple example", "Complex example", "Real-life usage"]
        )
        self._add_section(
            "🎯 Practice",
            ["Do it yourself", "Typical tasks (fill in the blanks, translation, multiple choice)"]
        )
        self._add_section(
            "⚡ Common Mistakes",
            ["Frequent confusions", "Beginner errors", "False friends in translation"]
        )
        self._add_section(
            "🌍 Vocabulary & Expressions",
            ["New words", "Collocations", "Idioms & phrasal verbs"]
        )
        self._add_section(
            "📐 Grammar in Depth",
            ["Tenses overview", "Modal verbs", "Conditionals"]
        )
        self._add_section(
            "🔗 Comparisons",
            ["With other tenses/structures", "With native language"]
        )
        self._add_section(
            "📚 Resources",
            ["Textbooks", "Articles & videos", "Dictionaries"]
        )
        self._add_section(
            "📝 Summary",
            ["Key rule", "3–5 takeaways"]
        )


class GermanTemplate(TemplateMd):
    """Template for studying German topics"""

    def __init__(self, title: str = "German Topic", emoticon: str = "🇩🇪", tags: Optional[list[str]] = None) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_german", tags=tags)

    def get_available_files(self, directory: Optional[str] = None, end: str = "_german.md") -> list[str]:
        return super().get_available_files(directory, end)

    def _structure(self) -> None:
        super()._structure()
        self._add_section(
            "📖 Einführung",
            ["Was ist das Thema?", "Wo wird es verwendet?", "Warum ist es wichtig?"]
        )
        self._add_section(
            "🔑 Regeln & Struktur",
            ["Hauptregel", "Ausnahmen", "Tabellen (z. B. Deklinationen)"]
        )
        self._add_section(
            "📝 Beispiele",
            ["Einfaches Beispiel", "Komplexeres Beispiel", "Alltägliche Sprache"]
        )
        self._add_section(
            "🎯 Übungen",
            ["Selbst üben", "Typische Aufgaben (Lücken, Übersetzung, Multiple Choice)"]
        )
        self._add_section(
            "⚡ Häufige Fehler",
            ["Verwechslungen", "Fehler bei Anfängern", "Falsche Freunde"]
        )
        self._add_section(
            "🌍 Wortschatz & Ausdrücke",
            ["Neue Wörter", "Kollokationen", "Redewendungen"]
        )
        self._add_section(
            "📐 Grammatik im Detail",
            ["Artikel & Fälle", "Satzstellung", "Starke und schwache Verben"]
        )
        self._add_section(
            "🔗 Vergleiche",
            ["Mit anderen Themen", "Mit der Muttersprache"]
        )
        self._add_section(
            "📚 Quellen",
            ["Lehrbücher", "Artikel & Videos", "Wörterbücher"]
        )
        self._add_section(
            "📝 Zusammenfassung",
            ["Wichtigste Regel", "3–5 Kernaussagen"]
        )

class FrenchTemplate(TemplateMd):
    """Template for studying French topics"""

    def __init__(self, title: str = "French Topic", emoticon: str = "🇫🇷", tags: Optional[list[str]] = None) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_french", tags=tags)

    def get_available_files(self, directory: Optional[str] = None, end: str = "_french.md") -> list[str]:
        return super().get_available_files(directory, end)

    def _structure(self) -> None:
        super()._structure()
        self._add_section(
            "📖 Introduction",
            ["Quel est le sujet ?", "Où est-il utilisé ?", "Pourquoi est-il important ?"]
        )
        self._add_section(
            "🔑 Règles & Structure",
            ["Règle principale", "Exceptions", "Tableaux (par ex. conjugaisons)"]
        )
        self._add_section(
            "📝 Exemples",
            ["Exemple simple", "Exemple complexe", "Usage réel"]
        )
        self._add_section(
            "🎯 Exercices",
            ["À faire soi-même", "Exercices typiques (compléter, traduire, choix multiple)"]
        )
        self._add_section(
            "⚡ Erreurs courantes",
            ["Confusions fréquentes", "Fautes des débutants", "Faux amis"]
        )
        self._add_section(
            "🌍 Vocabulaire & Expressions",
            ["Mots nouveaux", "Collocations", "Expressions idiomatiques"]
        )
        self._add_section(
            "📐 Grammaire en profondeur",
            ["Prononciation & accents", "Articles", "Conjugaison des verbes"]
        )
        self._add_section(
            "🔗 Comparaisons",
            ["Avec d'autres temps/thèmes", "Avec la langue maternelle"]
        )
        self._add_section(
            "📚 Ressources",
            ["Manuels", "Articles & vidéos", "Dictionnaires"]
        )
        self._add_section(
            "📝 Résumé",
            ["Règle clé", "3–5 points essentiels"]
        )


class SpanishTemplate(TemplateMd):
    """Template for studying Spanish topics"""

    def __init__(self, title: str = "Spanish Topic", emoticon: str = "🇪🇸", tags: Optional[list[str]] = None) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_spanish", tags=tags)

    def get_available_files(self, directory: Optional[str] = None, end: str = "_spanish.md") -> list[str]:
        return super().get_available_files(directory, end)

    def _structure(self) -> None:
        super()._structure()
        self._add_section(
            "📖 Introducción",
            ["¿Cuál es el tema?", "¿Dónde se usa?", "¿Por qué es importante?"]
        )
        self._add_section(
            "🔑 Reglas & Estructura",
            ["Regla principal", "Excepciones", "Tablas de referencia"]
        )
        self._add_section(
            "📝 Ejemplos",
            ["Ejemplo sencillo", "Ejemplo más complejo", "Uso real"]
        )
        self._add_section(
            "🎯 Práctica",
            ["Hazlo tú mismo", "Ejercicios típicos (completar, traducir, opción múltiple)"]
        )
        self._add_section(
            "⚡ Errores comunes",
            ["Confusiones frecuentes", "Errores de principiantes", "Falsos amigos"]
        )
        self._add_section(
            "🌍 Vocabulario & Expresiones",
            ["Palabras nuevas", "Colocaciones", "Expresiones idiomáticas"]
        )
        self._add_section(
            "📐 Gramática en profundidad",
            ["Conjugación de verbos (AR/ER/IR)", "Tiempos verbales", "Subjuntivo"]
        )
        self._add_section(
            "🔗 Comparaciones",
            ["Con otros tiempos/temas", "Con la lengua materna"]
        )
        self._add_section(
            "📚 Recursos",
            ["Libros de texto", "Artículos & videos", "Diccionarios"]
        )
        self._add_section(
            "📝 Resumen",
            ["Regla clave", "3–5 ideas principales"]
        )

class BookTemplate(TemplateMd):
    """Шаблон для конспектирования книг"""

    def __init__(self, title: str = "Название книги", author: str = "Автор", emoticon: str = "📚", tags: Optional[list[str]] = None) -> None:
        self.__author = author
        super().__init__(title=title, emoticon=emoticon, suffix="_book", tags=tags)

    def get_available_files(self, directory: Optional[str] = None, end: str = "_book.md") -> list[str]:
        return super().get_available_files(directory, end)
        
    def _structure(self) -> None:
        super()._structure()
        # Добавляем информацию об авторе
        self._add_section(
            "👤 Автор",
            [self.__author]
        )
        
        self._add_section(
            "📋 Основная информация",
            [
                "Год публикации:",
                "Жанр:",
                "Ключевые темы:",
                "Основные идеи:"
            ]
        )
        
        self._add_section(
            "🎯 Тезис книги",
            ["Основная мысль, которую доносит автор:"]
        )
        
        self._add_section(
            "📖 Краткое содержание",
            [
                "Глава 1:",
                "Глава 2:",
                "Глава 3:"
                # Можно добавить больше глав
            ]
        )
        
        self._add_section(
            "💡 Ключевые цитаты",
            [
                "Цитата 1 (с пояснением):",
                "Цитата 2 (с пояснением):",
                "Цитата 3 (с пояснением):"
            ]
        )
        
        self._add_section(
            "🔍 Анализ и критика",
            [
                "Сильные стороны книги:",
                "Слабые стороны книги:",
                "С чем согласен:",
                "С чем не согласен:"
            ]
        )
        
        self._add_section(
            "🌍 Влияние и значение",
            [
                "Исторический контекст:",
                "Влияние на современность:",
                "Актуальность сегодня:"
            ]
        )
        
        self._add_section(
            "🤔 Личные выводы",
            [
                "Что я узнал нового:",
                "Как изменилось мое мнение:",
                "Как применю эти знания:"
            ]
        )
        
        self._add_section(
            "🔗 Связанные материалы",
            [
                "Другие книги автора:",
                "Похожие книги:",
                "Статьи/рецензии:"
            ]
        )


class PhilosophyTemplate(TemplateMd):
    """Шаблон для философских концепций"""

    def __init__(self, title: str = "Философская концепция", emoticon: str = "🧠", tags: Optional[list[str]] = None) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_philosophy", tags=tags)

    def get_available_files(self, directory: Optional[str] = None, end: str = "_philosophy.md") -> list[str]:
        return super().get_available_files(directory, end)

    def _structure(self) -> None:
        super()._structure()
        
        self._add_section(
            "🤫 Основные представители",
            [
                "Философ 1:",
                "Философ 2:",
                "Философ 3:"
            ]
        )
        
        self._add_section(
            "🕰️ Исторический контекст",
            [
                "Период:",
                "Предшествующие идеи:",
                "Последующие влияния:"
            ]
        )
        
        self._add_section(
            "📝 Ключевые понятия",
            [
                "Понятие 1 (определение):",
                "Понятие 2 (определение):",
                "Понятие 3 (определение):"
            ]
        )
        
        self._add_section(
            "💭 Основные тезисы",
            [
                "Тезис 1:",
                "Тезис 2:",
                "Тезис 3:"
            ]
        )
        
        self._add_section(
            "🔄 Диалектика развития",
            [
                "Тезис:",
                "Антитезис:",
                "Синтез:"
            ]
        )
        
        self._add_section(
            "❗ Критика и контраргументы",
            [
                "Критика 1:",
                "Критика 2:",
                "Ответы на критику:"
            ]
        )
        
        self._add_section(
            "🌍 Применение и влияние",
            [
                "В политике:",
                "В культуре:",
                "В науке:",
                "В повседневной жизни:"
            ]
        )
        
        self._add_section(
            "📚 Основные произведения",
            [
                "Книга 1:",
                "Книга 2:",
                "Книга 3:"
            ]
        )
        
        self._add_section(
            "🤔 Современная интерпретация",
            [
                "Актуальность сегодня:",
                "Современные последователи:",
                "Неоиспользование концепции:"
            ]
        )


class HistoryTemplate(TemplateMd):
    """Шаблон для исторических событий и периодов"""

    def __init__(self, title: str = "Историческое событие", emoticon: str = "🏛️", tags: Optional[list[str]] = None) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_history", tags=tags)
    
    def get_available_files(self, directory: Optional[str] = None, end: str = "_history.md") -> list[str]:
        return super().get_available_files(directory, end)

    def _structure(self) -> None:
        super()._structure()
        
        self._add_section(
            "📅 Хронология",
            [
                "Дата начала:",
                "Дата окончания:",
                "Ключевые даты:"
            ]
        )
        
        self._add_section(
            "🗺️ Географический контекст",
            [
                "Место:",
                "Территория:",
                "Геополитический контекст:"
            ]
        )
        
        self._add_section(
            "🤫 Ключевые участники",
            [
                "Персона 1 (роль):",
                "Персона 2 (роль):",
                "Персона 3 (роль):"
            ]
        )
        
        self._add_section(
            "📋 Предпосылки и причины",
            [
                "Экономические причины:",
                "Политические причины:",
                "Социальные причины:",
                "Культурные причины:"
            ]
        )
        
        self._add_section(
            "📖 Основные события",
            [
                "Событие 1:",
                "Событие 2:",
                "Событие 3:",
                "Событие 4:"
            ]
        )
        
        self._add_section(
            "🎯 Итоги и последствия",
            [
                "Краткосрочные последствия:",
                "Долгосрочные последствия:",
                "Изменения на карте мира:",
                "Демографические изменения:"
            ]
        )
        
        self._add_section(
            "📊 Историческое значение",
            [
                "Влияние на будущие события:",
                "Изменение баланса сил:",
                "Культурное наследие:"
            ]
        )
        
        self._add_section(
            "📚 Источники и интерпретации",
            [
                "Основные источники:",
                "Разные исторические школы:",
                "Современные интерпретации:"
            ]
        )
        
        self._add_section(
            "🔍 Дискуссионные вопросы",
            [
                "Спорные моменты:",
                "Альтернативные точки зрения:",
                "Неразрешенные вопросы:"
            ]
        )

        
class PhysicsTemplate(TemplateMd):
    """Шаблон для физических концепций и законов"""

    def __init__(self, title: str = "Физическая концепция", emoticon: str = "⚛️", tags: Optional[list[str]] = None) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_physics", tags=tags)

    def get_available_files(self, directory: Optional[str] = None, end: str = "_physics.md") -> list[str]:
        return super().get_available_files(directory, end)

    def _structure(self) -> None:
        super()._structure()
        
        self._add_section(
            "📝 Формулировка",
            ["Основная формулировка закона/принципа:"]
        )
        
        self._add_section(
            "📏 Математическое выражение",
            ["Формулы:", "Уравнения:", "Вывод формул:"]
        )
        
        self._add_section(
            "⚙️ Физический смысл",
            ["Что описывает:", "Какие явления объясняет:"]
        )
        
        self._add_section(
            "🔍 Экспериментальное подтверждение",
            [
                "Кто открыл/доказал:",
                "Ключевые эксперименты:",
                "Оборудование для демонстрации:"
            ]
        )
        
        self._add_section(
            "📐 Единицы измерения",
            ["Основные единицы:", "Производные единицы:"]
        )
        
        self._add_section(
            "🔄 Практическое применение",
            [
                "В технике:",
                "В технологии:",
                "В повседневной жизни:"
            ]
        )
        
        self._add_section(
            "❗ Ограничения и исключения",
            [
                "Где не работает:",
                "Условия применимости:",
                "Пограничные случаи:"
            ]
        )
        
        self._add_section(
            "🔗 Связь с другими разделами физики",
            [
                "С механикой:",
                "С термодинамикой:",
                "С электродинамикой:",
                "С квантовой физикой:"
            ]
        )
        
        self._add_section(
            "🧪 Лабораторные работы",
            ["Возможные эксперименты для подтверждения:"]
        )
        
        self._add_section(
            "🎓 Углубленное изучение",
            [
                "Сложные аспекты:",
                "Современные исследования:",
                "Неразрешенные вопросы:"
            ]
        )


class AstronomyTemplate(TemplateMd):
    """Шаблон для астрономических объектов и явлений"""

    def __init__(self, title: str = "Астрономический объект", emoticon: str = "🌌", tags: Optional[list[str]] = None) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_astronomy", tags=tags)

    def get_available_files(self, directory: Optional[str] = None, end: str = "_astronomy.md") -> list[str]:
        return super().get_available_files(directory, end)

    def _structure(self) -> None:
        super()._structure()
        
        self._add_section(
            "⭐ Основные характеристики",
            [
                "Тип объекта:",
                "Размеры:",
                "Масса:",
                "Расстояние от Земли:"
            ]
        )
        
        self._add_section(
            "🪐 Физические свойства",
            [
                "Состав:",
                "Температура:",
                "Плотность:",
                "Сила тяжести:"
            ]
        )
        
        self._add_section(
            "🌀 Движение и орбита",
            [
                "Период обращения:",
                "Скорость движения:",
                "Наклон орбиты:",
                "Эксцентриситет:"
            ]
        )
        
        self._add_section(
            "👁️ Наблюдение",
            [
                "Видимая звездная величина:",
                "Лучшее время для наблюдения:",
                "Необходимое оборудование:",
                "История открытия:"
            ]
        )
        
        self._add_section(
            "🔭 Исследование",
            [
                "Кто открыл:",
                "Миссии по изучению:",
                "Основные discoveries:"
            ]
        )
        
        self._add_section(
            "🌠 Особенности и аномалии",
            [
                "Уникальные свойства:",
                "Необъяснимые явления:",
                "Загадки и тайны:"
            ]
        )
        
        self._add_section(
            "📊 Сравнение с аналогичными объектами",
            [
                "Сходства:",
                "Различия:",
                "Место в классификации:"
            ]
        )
        
        self._add_section(
            "🔮 Значение и влияние",
            [
                "Влияние на Землю:",
                "Роль в эволюции Вселенной:",
                "Культурное значение:"
            ]
        )
        
        self._add_section(
            "🎓 Современные исследования",
            [
                "Актуальные научные вопросы:",
                "Планируемые миссии:",
                "Перспективы изучения:"
            ]
        )


class SocialScienceTopic(TemplateMd):
    """Создает шаблон для тем по обществознанию как науке"""

    def __init__(self, title: str = "Название темы", emoticon: str = "🏛️", tags: Optional[list[str]] = None) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_socialscience", tags=tags)

    def get_available_files(self, directory: Optional[str] = None, end: str = "_socialscience.md") -> list[str]:
        return super().get_available_files(directory, end)

    def _structure(self) -> None:
        super()._structure()

        self._add_section(
            "😸 Общее представление",
            [
                "Что изучает данная тема в обществознании?",
                "Почему это важно?",
                "Какие ключевые вопросы решаются?",
                "Связь темы с реальной жизнью и обществом"
            ]
        )

        self._add_section(
            "😺 Понятия и термины",
            [
                "Термин 1 — определение",
                "Термин 2 — определение",
                "Термин 3 — определение"
            ]
        )

        self._add_section(
            "😼 Теории и подходы",
            [
                "Теория 1 — описание и применение",
                "Теория 2 — описание и применение",
                "Методы исследования (социологические, экономические, политические)"
            ]
        )


        self._add_section(
            "😾 Примеры и кейсы",
            [
                "Исторический пример",
                "Современный пример из общества или политики",
                "Сравнительный пример между странами или регионами"
            ]
        )


        self._add_section(
            "🐯 Практика",
            [
                "Анализ текстов, статей, исследований",
                "Составление собственных выводов",
                "Построение схем, диаграмм или таблиц для визуализации"
            ]
        )

        self._add_section(
            "😡 Подводные камни и ошибки",
            [
                "Распространенные заблуждения",
                "Ошибки интерпретации данных",
                "Особенности, которые легко пропустить"
            ]
        )


        self._add_section(
            "🧐 Сравнение & аналоги",
            [
                "Сравнение различных социологических теорий",
                "Аналогии с экономикой, политологией, культурологией"
            ]
        )

        self._add_section(
            "😶 Связанные темы",
            [
                "Политология, экономика, право",
                "Социальная психология, культурология",
                "История и философия общества"
            ]
        )

        self._add_section(
            "🤓 Полезные источники",
            [
                "Учебники и статьи по обществознанию",
                "Научные публикации, исследования",
                "Видео, лекции, курсы"
            ]
        )

        self._add_section(
            "😤 Итоги",
            [
                "Краткое резюме темы",
                "Главные выводы и инсайты",
                "Что применить для дальнейшего изучения"
            ]
        )


class LawTopic(TemplateMd):
    """Создает шаблон для тем по праву с возможностью указания дополнительных идентификаторов"""

    def __init__(
        self,
        title: str = "Название темы/документа",
        doc_number: Optional[str] = None,
        year: Optional[str] = None,
        law_type: Optional[str] = None,
        short_name: Optional[str] = None,
        tags: Optional[list[str]] = None,
        emoticon: str = "⚖️"
    ) -> None:


        self.__doc_number = doc_number
        self.__year = year
        self.__law_type = law_type
        self.__short_name = short_name
        super().__init__(title=title, emoticon=emoticon, suffix="_law", tags=tags)
    
    def get_available_files(self, directory: Optional[str] = None, end: str = "_law.md") -> list[str]:
        return super().get_available_files(directory, end)
        
    def _structure(self) -> None:
        super()._structure()
        # Вот так тоже можно делать.
        # Прямо в классе создать список и забросить его в секцию
        general_info: list[str] = []
        if self.__short_name:
            general_info.append("Короткое название: " + self.__short_name)
        if self.__doc_number:
            general_info.append("Номер документа: " + self.__doc_number)
        if self.__year:
            general_info.append("Год принятия: " + self.__year)
        if self.__law_type:
            general_info.append("Область права: " + self.__law_type)

        self._add_section("😸 Общая информация", general_info)

        self._add_section(
            "😺 Понятия и термины",
            [
                "Термин 1 — определение",
                "Термин 2 — определение"
            ]
        )

        self._add_section(
            "📃Структура документа",
            [
                "Основные статьи и разделы",
                "Ключевые нормы и положения",
                "Примечания и ссылки на смежные статьи/акты"
            ]
        )

        self._add_section(
            "😾 Примеры",
            [
                "Пример из практики",
                "Применение нормы на реальном примере",
            ],
        )

        self._add_section(
            "🔍 Практический анализ",
            [
                "Разбор спорных моментов",
                "Комментарии и выводы"
            ]
        )

        self._add_section(
            "😡 Подводные камни и ошибки",
            [
                "Частые ошибки при толковании",
                "Особенности применения нормы"
            ]
        )

        self._add_section(
            "😤 Итоги",
            [
                "Краткое резюме документа",
                "Главные выводы"
            ]
        )


class EconomyTopic(TemplateMd):
    """Создает шаблон для тем по экономике как науке"""

    def __init__(self, title: str = "Название темы", emoticon: str = "📊", tags: Optional[list[str]] = None) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_economy", tags=tags)

    def get_available_files(self, directory: Optional[str] = None, end: str = "_economy.md") -> list[str]:
        return super().get_available_files(directory, end)

    def _structure(self) -> None:
        super()._structure()

        self._add_section(
            "🏡 Общее представление",
            [
                "Что изучает данная тема в экономике?",
                "Почему это важно?",
                "Какие ключевые вопросы решаются?",
                "Как тема связана с реальной экономикой?"
            ]
        )

        self._add_section(
            "😺 Понятия и термины",
            [
                "Термин 1 — определение",
                "Термин 2 — определение",
                "Термин 3 — определение"
            ]
        )

        self._add_section(
            "😼 Теории и модели",
            [
                "Модель 1 — описание и применение",
                "Модель 2 — описание и применение",
                "Краткая формула или графическая схема, если есть"
            ]
        )

        self._add_section(
            "😾 Примеры использования",
            [
                "Простой пример (наглядное объяснение)",
                "Сложный пример (комплексная ситуация)",
                "Практический пример из экономики страны/рынка"
            ]
        )

        self._add_section(
            "🐯 Практика",
            [
                "Рассчитать показатели (если есть формулы)",
                "Построить график / диаграмму (matplotlib)",
                "Составить свой мини-анализ"
            ]
        )

        self._add_section(
            "😡 Подводные камни и ошибки",
            [
                "Частые заблуждения при изучении темы",
                "Ошибки при расчётах или интерпретации данных",
                "Особенности, которые легко пропустить"
            ]
        )

        self._add_section(
            "🧐 Сравнение & аналоги",
            [
                "Сравнение с другими экономическими теориями или моделями",
                "Аналогии с реальными примерами бизнеса или рынка"
            ]
        )

        self._add_section(
            "😶 Связанные темы",
            [
                "Микроэкономика / макроэкономика",
                "Финансовые рынки",
                "Статистика и аналитика",
                "Политическая экономия, государственная политика"
            ]
        )

        self._add_section(
            "🤓 Полезные источники",
            [
                "Классические учебники по экономике",
                "Статьи и публикации",
                "Видео и лекции",
                "Собственные заметки и примеры"
            ]
        )

        self._add_section(
            "😤 Итоги",
            [
                "Краткое резюме темы",
                "3–5 ключевых выводов",
                "Что применить на практике или изучить глубже"
            ]
        )


class RecipeTopic(TemplateMd):
    """Создает шаблон для заметок по кулинарии/рецептам"""

    def __init__(self, title: str = "Название рецепта", emoticon: str = "🍳", tags: Optional[list[str]] = None) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_recipe", tags=tags)

    def get_available_files(self, directory: Optional[str] = None, end: str = "_recipe.md") -> list[str]:
        return super().get_available_files(directory, end)

    def _structure(self) -> None:
        super()._structure()

        self._add_section(
            "🍓 Общее представление",
            [
                "Название блюда",
                "Тип блюда (завтрак, обед, ужин, десерт)",
                "Время приготовления",
                "Сложность",
                "Количество порций"
            ]
        )

        self._add_section(
            "🍒 Ингредиенты",
            [
                "Список необходимых продуктов с указанием количества",
                "Дополнительно: заменители ингредиентов"
            ]
        )

        self._add_section(
            "🍴 Приготовление",
            [
                "Пошаговая инструкция",
                "Важные нюансы или советы",
                "Температуры и время готовки, если применимо"
            ]
        )

        self._add_section(
            "🍏🍎 Варианты и модификации",
            [
                "Возможные изменения рецепта",
                "Замена ингредиентов",
                "Советы по украшению и подаче"
            ]
        )

        self._add_section(
            "🥃 Подводные камни и ошибки",
            [
                "На что обращать внимание при приготовлении",
                "Что часто идет не так и как исправить"
            ]
        )

        self._add_section(
            "🥛🐟 Сочетания и советы",
            [
                "С какими блюдами хорошо подавать",
                "Напитки и соусы",
                "Сервировка и хранение"
            ]
        )

        self._add_section(
            "🌍 Источники",
            [
                "Ссылка на оригинальный рецепт, если есть",
                "Кулинарные книги или видео",
                "Личный опыт и заметки"
            ]
        )

        self._add_section(
            "🍽️ Итоги",
            [
                "Краткое резюме рецепта",
                "Главные выводы и советы",
                "Что можно попробовать изменить в следующий раз"
            ]
        )


class PersonalWorldviewTopic(TemplateMd):
    """Создает шаблон для заметок 'Личное понимание мира' / Personal Worldview"""

    def __init__(self, title: str = "Название темы", emoticon: str = "🌏", tags: Optional[list[str]] = None) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_worldview", tags=tags)

    def get_available_files(self, directory: Optional[str] = None, end: str = "_worldview.md") -> list[str]:
        return super().get_available_files(directory, end)

    def _structure(self) -> None:
        super()._structure()

        self._add_section(
            "🌌 Общая информация",
            [
                "Название темы/раздела",
                "Дата записи",
                "Источник вдохновения (книга, курс, лекция, наблюдение)"
            ]
        )


        self._add_section(
            "💡 Основная идея",
            [
                "Краткое резюме ключевой мысли",
                "Почему это важно лично для меня"
            ]
        )

        self._add_section(
            "⚙️ Детальный разбор",
            [
                "Подтема 1 — описание и размышления",
                "Подтема 2 — описание и размышления",
                "Подтема 3 — описание и размышления"
            ]
        )


        self._add_section(
            "⚖️ Практические выводы",
            [
                "Что можно применить на практике",
                "Привычки или действия, которые стоит попробовать",
                "Эксперименты над собой или наблюдения"
            ]
        )

        self._add_section(
            "❓ Вопросы для себя",
            [
                "Что ещё можно изучить по этой теме",
                "Какие вопросы помогают глубже понять тему",
                "Что остаётся непонятным и требует размышления"
            ]
        )

        self._add_section(
            "📎 Связанные идеи и источники",
            [
                "Связанные темы или заметки",
                "Книги, статьи, видео, курсы",
                "Собственные наблюдения и выводы"
            ]
        )

        self._add_section(
            "😏 Итоговые мысли",
            [
                "Краткое резюме темы",
                "Главные выводы и инсайты",
                "Что применить в будущем"
            ]
        )

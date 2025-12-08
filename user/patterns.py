from core.lib.templates.patterns import TemplateMd

class Library(TemplateMd):
    """Создает шаблон для библиотек по программированию (python)"""

    def __init__(self, title: str = "Название библиотеки", emoticon: str = "🐍", tags: list[str] | None = None) -> None:
        super().__init__(title=title, emoticon=emoticon, suffix="_library", tags=tags)

    def get_available_files(self, directory: str | None = None, end: str = "_library.md") -> list[str]:
        return super().get_available_files(directory, end)
    
    def structure(self) -> None:
        super().structure()
        self.add_section(
            "😸 ГЛАВА 1. ОБЩЕЕ ПРЕДСТАВЛЕНИЕ БИБЛИОТЕКИ",
            [
                "**Описание библиотеки:**",
                "**Альтернативы библиотеки и сравнение:**"
            ]
        )
        
        self.add_section(
            "😺 ГЛАВА 2. УСТАНОВКА И НАСТРОЙКА",
            [
                "**Установка:**",
                "**Проверка работоспособности:**",
                "**Ссылки на документацию:**"
            ]
        )
        
        self.add_section(
            "😼 ГЛАВА 3. БАЗОВОЕ ИСПОЛЬЗОВАНИЕ БИБЛИОТЕКИ",
            [
                "**Простейший пример:**",
                "**Ключевые объекты, классы, функции:**",
                "**Основные методы и атрибуты:**"
            ]
        )
        
        self.add_section(
            "😾 ГЛАВА 4. ПРАКТИЧЕСКОЕ ПРИМЕНЕНИЕ БИБИОТЕКИ",
            [
                "**Практический пример:**",
                "**Своё практическое применение:**"
            ]
        )
        
        self.add_section(
            "😽 ГЛАВА 5. РАЗБОР СЛОЖНЫХ МОМЕНТОВ",
            [
                "**Ошибки:**",
                "**Логика изнутри:**",
                "**Как расширяется:**"
            ]
        )
        
        self.add_section(
            "😿 ГЛАВА 6. ПРОЕКТ И ПРАКТИКА",
            [
                "**Свой проект:**",
                "**Упаковка в шаблон:**"
            ]
        )
        
        self.add_section(
            "🙀 ГЛАВА 7. ДОКУМЕНТАЦИЯ И ЗАКРЕПЛЕНИЕ",
            [
                "**Обзор официальной документации:**",
                "**Закладки с полезными ссылками:**",
                "**Личный конспект:**"
            ]
        )
        
        self.add_section(
            "😻 ГЛАВА 8. ИТОГ",
            [
                "**Понятно:**",
                "**Не понятно:**",
                "**Что дальше:**"
            ]
        )


class MyTemplate(TemplateMd):
    def __init__(self, *, title: str = "Название титульника", tags: list[str] | None = None, emoticon: str = "📝", suffix: str = "") -> None:
        super().__init__(title=title, tags=tags, emoticon=emoticon, suffix=suffix)

    def get_available_files(self, directory: str | None = None, end: str = ".md") -> list[str]:
        return super().get_available_files(directory, end)
    
    def structure(self) -> None:
        super().structure()
        # self.add_section()
        # self.add_code_section()


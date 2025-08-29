"""acrions.py

Имеет класс контейнер, содержащий методы, которые имею возможность вызова из меню.
"""

import os
import sys
import shutil
import subprocess
import json
from typing import Any, Optional, Type, TypeVar

from rich.console import Console
from rich.text import Text

from core.lib.patterns import *
from core.lib.prompts import Prompts, PromptsDict, PromptSite, Errors, PromptsLaw, main_color, support_color
from core.lib.dictionary import Dictionary, interactive_mode

from core.lib.system_apps.findler import findler
from core.lib.system_apps.back import backup

# Для аннотации
TemplateClass = TypeVar("TemplateClass", bound="TemplateMd")

class CLI:
    """Класс-контейнер. Содержит в себе множественные объекты классов."""
    def __init__(self, paths: Optional[dict[str, str]] = None) -> None:
       
        """Содержит важные поля и объекты для работы"""
        directory = "Storage"
        # Для поддержания работы в кросс-платформенном режиме
        self.__linux = sys.platform.startswith("linux")
        self.__darwin = sys.platform.startswith("darwin")
        self.__windows = sys.platform.startswith("win")

        #
        # Получаем полное расположение файла, чтобы создать папку рядом.
        self.current_file = os.path.abspath(__file__)
        # Поднимаемся на три папки выше отсюда.
        # base_path - путь к основной папке, где лежит __main__.py.
        # Рядом будет создана
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(self.current_file)))
        self.menu_path = os.path.join(self.base_path, "menu.json")
        self.config_path = os.path.join(self.base_path, "config.json")
        self.actions_path = os.path.join(self.base_path, "actions.json")
        # Вывести цветной текст
        self.__console = Console()
        # Дефолтные пути, если в json ничего нет
        # Создаст папку рядом с __main__.py с названием Storage
        

        self.paths = {
            "topic": os.path.join(self.base_path, directory, "Topics"),
            "library": os.path.join(self.base_path, directory, "Libraries"),
            "html": os.path.join(self.base_path, directory, "HTML_Topics"),
            "css": os.path.join(self.base_path, directory, "CSS_Topics"),
            "js": os.path.join(self.base_path, directory,"JS_Topics"),
            "english": os.path.join(self.base_path, directory, "English"),
            "german": os.path.join(self.base_path, directory, "German"),
            "french": os.path.join(self.base_path, directory, "French"),
            "spanish": os.path.join(self.base_path, directory, "Spanish"),
            "dictionary": os.path.join(self.base_path, directory, "Languages","dictionary.md"),
            "backup": os.path.join(self.base_path, directory, "Languages","Backup"),
            "books": os.path.join(self.base_path, directory, "Books"),
            "recipe": os.path.join(self.base_path, directory, "Recipe"),
            "worldview":  os.path.join(self.base_path, directory, "Recipe"),
            "history": os.path.join(self.base_path, directory, "History"),
            "philosophy": os.path.join(self.base_path, directory, "Philosophy"),
            "socialscience": os.path.join(self.base_path, directory, "SocialScience"),
            "economy": os.path.join(self.base_path, directory, "Economy"),
            "law": os.path.join(self.base_path, directory, "Law"),
            "physics": os.path.join(self.base_path, directory, "Physics"),
            "astronomy": os.path.join(self.base_path, directory, "Astronomy")
        }
        
        # Если переданы настройки json
        # Обновляем
        # Эта строчка позволяет обойти ошибку (и баг), если в json ничего не будет
        if paths is not None:
            self.paths.update(paths)
        else:
            try:
                self.paths.update(self.load_paths())
            except FileNotFoundError:
                pass

        # Создаем вот такие папки, а .md пропускаем
        # Откуда взялся .md? Это путь к "dictionary.md" - словарь с языками
        # (не python словарь, а в прямом смысле словарь)
        for _, path in self.paths.items():
            if not path.endswith(".md"):
                os.makedirs(path, exist_ok=True)
    
    def create_item(self, *, cls: Type[TemplateClass], title_prompt: Text, path_key: str, extra_arguments: Optional[list[tuple[str, Text]]] = None):
        # Запрашиваем название
        self.__console.print(title_prompt)
        title = self.__console.input(Prompts.arrows)
        # Запрашиваем теги
        tags = self.input_tags()
        # Дополнительные поля
        extra_args: dict[str, Any] = {}
        if extra_arguments:
            for field_name, prompt in extra_arguments:
                self.__console.print(prompt)
                value = self.__console.input(Prompts.arrows).strip() or None
                extra_args[field_name] = value
        
        # Создаем объект
        item: TemplateClass = cls(title=title, tags=tags, **extra_args)
        # Путь по умолчанию и сохранение
        self.__console.print(Prompts.save, Prompts.file_name, Prompts.save_path, Prompts.enter, Prompts.default)
        item.set_default_path(self.paths[path_key])
        path_name = self.__console.input(Prompts.arrows) or None
        item.start(path_name)

    def look_item(self, *, cls: Type[TemplateClass], path_key: str):
        item = cls() # Создаем новый экземпляр класса.
        files = item.get_available_files(self.paths[path_key]) # Сюда тоже следует закинуть путь по дефолту
        self.__support_md_loop(files)

    def load_paths(self):

        with open(self.config_path, "r", encoding="UTF-8") as f:
            config_raw = json.load(f)

        # Преобразуем ключи и значения в str
        paths: dict[str, str] = {}
        for k, v in config_raw.get("paths", {}).items():
            paths[str(k)] = str(v)
        return paths

    def input_tags(self, prompt: Text = Prompts.tags, input_prompt: Text = Prompts.arrows) -> Optional[list[str]]:
        # Конструкция, запрашивающая теги
        self.__console.print(prompt)
        tags: Optional[list[str]] = []
        while True:
            tag = self.__console.input(input_prompt).strip()
            if not tag:
                break
            tags.append(tag)
        
        return tags or None

        # Окончание конструкции, запрашивающей теги
        # Передаем в аргументы название и теги.
        #### Также, сюда можно ввести эмодзи emoticon
    
    def __support_md_loop(self, md_files: list[str]) -> None:
        """Вспомогательный метод. Сокращает код.

        Предназначен для покраски цифр в цикле
        """
        for item, names in enumerate(md_files, 1):
            self.__console.print(Text(f"{item}. ", style=support_color) + Text(names, style=main_color))
    
    def __support_page(self, command: str):
        """Вспомогательный метод для открытия веб-страниц в браузере."""
        if self.__windows:
            subprocess.Popen(f"start {command}", shell=True)
        elif self.__darwin:
            subprocess.Popen(f"open {command}", shell=True)
        elif self.__linux:
            subprocess.Popen(f"bash -c 'xdg-open {command}'", shell=True)
        else:
            self.__console.print(PromptSite.functional)
    
    def __support_open_app(self, command: str):
        """Вспомогательный метод для открытия приложений на устройстве"""
        if self.__windows:
            subprocess.Popen(f'start "" "{command}"', shell=True)
        elif self.__darwin:
            subprocess.Popen(f'open -a "{command}"', shell=True)
        elif self.__linux:
            subprocess.Popen([command])
        else:
            self.__console.print(PromptSite.functional)
    ###########################################################
    def open_page(self):
        """Метод, открывающий страницу в браузере. Необходим ввод ссылки пользователем"""
        self.__console.print(PromptSite.link)
        site = self.__console.input(Prompts.arrows)
        self.__support_page(site)
    ###########################################################
    def open_google(self):
        # Мы можем также хранить ссылки в json файле
        """Метод, открывающий поисковик Google"""
        self.__support_page("https://www.google.com")
    
    def open_youtube(self):
        """Метод, открывающий YouTube"""
        self.__support_page("https://www.youtube.com")
    ###########################################################
    def open_udemy(self):
        """Метод, октрывающий сайт Udemy"""
        self.__support_page("https://www.udemy.com")
    ###########################################################
    ###########################################################
    ###########################################################
    def create_topic(self):
        """Создает шаблон для тем по программированию (python)
        """
        self.create_item(cls=Topic, title_prompt=Prompts.theme, path_key="topic")

    def look_topic(self):
        self.look_item(cls=Topic, path_key="topic")
    ###########################################################
    def create_library(self):
        """Создает шаблон для библиотек по программированию (python)
        """
        self.create_item(cls=Library, title_prompt=Prompts.theme, path_key="library")

    def look_library(self):
        self.look_item(cls=Library, path_key="library")
    ###########################################################
    def create_html_topic(self):
        """Создает шаблон для тем по программированию (HTML)
        """
        self.create_item(cls=HTMLTopic, title_prompt=Prompts.theme, path_key="html")

    def look_html_topic(self):
        self.look_item(cls=HTMLTopic, path_key="html")
    ###########################################################
    def create_css_topic(self):
        self.create_item(cls=CssTopic, title_prompt=Prompts.theme, path_key="css")

    def look_css_topic(self):
        self.look_item(cls=CssTopic, path_key="css")
    ###########################################################
    def create_js_topic(self):
        """Создает шаблон для тем по программированию (js)
        """
        self.create_item(cls=JsTopic, title_prompt=Prompts.theme, path_key="js")

    def look_js_topic(self):
        self.look_item(cls=JsTopic, path_key="js")
    ###########################################################
    ###########################################################
    ###########################################################
    def english_topic(self):
        """Создает шаблон для изучения английского языка
        """
        self.create_item(cls=EnglishTemplate, title_prompt=Prompts.theme, path_key="english")

    def look_english(self):
        self.look_item(cls=EnglishTemplate, path_key="english")
    ###########################################################
    def german_topic(self):
        """Создает шаблон для изучения немецкого языка
        """
        self.create_item(cls=GermanTemplate, title_prompt=Prompts.theme, path_key="german")

    def look_german(self):
        self.look_item(cls=GermanTemplate, path_key="german")
    ###########################################################
    def french_topic(self):
        """Создает шаблон для изучения французского языка
        """
        self.create_item(cls=FrenchTemplate, title_prompt=Prompts.theme, path_key="french")

    def look_french(self):
        self.look_item(cls=FrenchTemplate, path_key="french")
    ###########################################################
    def spanish_topic(self):
        """Создает шаблон для изучения испанского языка
        """
        self.create_item(cls=SpanishTemplate, title_prompt=Prompts.theme, path_key="spanish")

    def look_spanish(self):
        self.look_item(cls=SpanishTemplate, path_key="spanish")
    ###########################################################
    def start_dict(self):
        # Словарь со словами
        md_file = self.paths["dictionary"]
        d = Dictionary()
        d.load_from_md(md_file)
        
        self.__console.print(f"\n{PromptsDict.loaded_words} {d.count_words()}")
        
        # Запуск интерактивного режима
        interactive_mode(d)
        backup()
    ###########################################################
    ###########################################################
    ###########################################################
    def watch_movie(self):
        print("from watch_movie")
    ###########################################################
    def open_steam(self):
        if self.__windows:
            try:
                self.__support_open_app("steam:/")
            except FileNotFoundError:
                possible_paths = [
                    "C:\\Program Files (x86)\\Steam\\Steam.exe",
                    "C:\\Program Files\\Steam\\Steam.exe"
                ]
                for path in possible_paths:
                    if os.path.exists(path):
                        self.__support_open_app(path)
                        break
                else:
                    self.__console.print(Errors.error_steam)

        elif self.__darwin:
            app_paths = ["/Applications/Steam.app", os.path.expanduser("~/Applications/Steam.app")]
            for path in app_paths:
                if os.path.exists(path):
                    self.__support_open_app(path)
                    break
            else:
                try:
                    self.__support_open_app("Steam")
                except FileNotFoundError:
                    self.__console.print(Errors.error_steam)

        elif self.__linux:
            path = shutil.which("steam")
            if path:
                self.__support_open_app(path)
            else:
                possible_paths = ["/usr/bin/steam", "/usr/local/bin/steam", "/snap/bin/steam"]
                for path in possible_paths:
                    if os.path.exists(path):
                        self.__support_open_app(path)
                        break
                else:
                    self.__console.print(Errors.error_steam)

        else:
            self.__console.print(Errors.error_steam)
    ###########################################################
    def open_book(self):
        print("from open_book")

    def write_book(self):
        """Создает шаблон для конспектирования книг
        """
        extra = [("author", Prompts.author)]
        self.create_item(cls=BookTemplate, title_prompt=Prompts.theme, path_key="books", extra_arguments=extra)

    def look_book(self):
        self.look_item(cls=BookTemplate, path_key="books")
    ###########################################################
    def recipe_topic(self):
        self.create_item(cls=RecipeTopic, title_prompt=Prompts.theme, path_key="recipe")

    def look_recipe(self):
        self.look_item(cls=RecipeTopic, path_key="recipe")
    ###########################################################
    def make_note(self):
        self.__console.print("form make_note", style=main_color)
    ###########################################################
    def make_world_note(self):
        self.create_item(cls=PersonalWorldviewTopic, title_prompt=Prompts.theme, path_key="worldview")
    
    def look_make_world_note(self):
        self.look_item(cls=PersonalWorldviewTopic, path_key="worldview")
    ###########################################################
    def history_topic(self):
        """Создает шаблон по историии
        """
        self.create_item(cls=HistoryTemplate, title_prompt=Prompts.theme, path_key="history")

    def look_history(self):
        self.look_item(cls=HistoryTemplate, path_key="history")
    ###########################################################
    def philosophy_topic(self):
        """Создает шаблон по философии
        """
        self.create_item(cls=PhilosophyTemplate, title_prompt=Prompts.theme, path_key="philosophy")

    def look_philosophy(self):
        self.look_item(cls=PhilosophyTemplate, path_key="philosophy")
    ###########################################################
    def socialscience_topic(self):
        self.create_item(cls=SocialScienceTopic, title_prompt=Prompts.theme, path_key="socialscience")
    
    def look_socialscience(self):
        self.look_item(cls=SocialScienceTopic, path_key="socialscience")
    ###########################################################
    def law_topic(self):
        extra = [
            ("doc_number", PromptsLaw.doc_number),
            ("short_name", PromptsLaw.short_name),
            ("year", PromptsLaw.year),
            ("law_type", PromptsLaw.law_type)
        ]
        self.create_item(cls=LawTopic, title_prompt=PromptsLaw.doc, path_key="law", extra_arguments=extra)

    def look_law(self):
        self.look_item(cls=LawTopic, path_key="law")
    ###########################################################
    def economy_topic(self):
        self.create_item(cls=EconomyTopic, title_prompt=Prompts.theme, path_key="economy")
    
    def look_economy(self):
        self.look_item(cls=EconomyTopic, path_key="economy")
    ###########################################################
    def physics_topic(self):
        """Создает шаблон для конспектирования книг
        """
        self.create_item(cls=PhysicsTemplate, title_prompt=Prompts.theme, path_key="physics")

    def look_physics(self):
        self.look_item(cls=PhysicsTemplate, path_key="physics")
    ###########################################################
    def astronomy_topic(self):
        """Создает шаблон для конспектирования книг
        """
        self.create_item(cls=AstronomyTemplate, title_prompt=Prompts.theme, path_key="astronomy")

    def look_astronomy(self):
        self.look_item(cls=AstronomyTemplate, path_key="astronomy")
    ###########################################################
    ###########################################################
    ###########################################################
    def find_file(self):
        # Системные функции
        # Поиск файлов (README) и сохранение по размеру
        findler()
    ###########################################################
    def monitoring(self):
        print("from monitoring")
    ###########################################################
    def activate_cerberus(self):
        print("your file is dead")
    ###########################################################
    ###########################################################
    ###########################################################
    def open_menu_settings(self):
        """Открывает настройки меню JSON"""
        self.__support_open_app(self.menu_path)

    def open_config_settings(self):
        """Открывает настройки путей JSON"""
        self.__support_open_app(self.config_path)
    
    def open_actions_settings(self):
        """Открывает настройки функций (!методов!) JSON"""
        self.__support_open_app(self.actions_path)

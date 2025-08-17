"""acrions.py

Содержит функции, вызываемые из меню.
"""
####! (import subprocess | import os | class MyClass_!ES!) - это намек. !####
from core.lib.prompts import Prompts
from core.lib.pattern import Topic, Library


def create_topic():
    """Создает шаблон для тем по программированию (python)
    """
    print(Prompts.theme)
    name = input(Prompts.arrows)
    topic = Topic(title=name)
    print(Prompts.save, Prompts.file_name, Prompts.save_path, Prompts.enter, Prompts.default)
    # topic.set_default_path("D:\\Python\\Topics\\Chapter")  # Путь по дефолту (активировать и изменить при необходимости)
    path_name = input(Prompts.arrows) or None
    topic.start(path_name)

def create_library():
    """Создает шаблон для библиотек по программированию (python)
    """
    print(Prompts.theme)
    name = input(Prompts.arrows)
    library = Library(title=name)
    print(Prompts.save, Prompts.file_name, Prompts.save_path, Prompts.enter, Prompts.default)
    # library.set_default_path("D:\\Python\\Library\\Libraries") # Путь по дефолту (активировать и изменить при необходимости)
    path_name = input(Prompts.arrows) or None
    library.start(path_name)

# Пустые функции. Оставил для наглядности (вот на сколько всё это можно расширить).
def create_js_topic():
    print("from create_js_topic")


def create_html_topic():
    print("from create_html_topic")


def create_css_topic():
    print("from create_css_topic")


def learn_english():
    print("from learn_english")


def learn_french():
    print("from learn_french")


def learn_german():
    print("from learn_german")


def learn_spanish():
    print("from learn_spanish")


def watch_movie():
    print("from watch_movie")


def play_game():
    print("from play_game")


def open_book():
    print("from open_book")


def write_book():
    print("from write_book")

def activate_cerberus():
    print("your file is dead")

# Обязательно в самом конце.
# Ключ и значение (в значении - ссылки на функции).
ACTIONS = {
    "create_topic":create_topic,
    "create_library": create_library,

    "create_js_topic": create_js_topic,
    "create_html_topic": create_html_topic,
    "create_css_topic": create_css_topic,

    "learn_english": learn_english,
    "learn_french": learn_french,
    "learn_german": learn_german,
    "learn_spanish": learn_spanish,

    "watch_movie": watch_movie,
    "play_game": play_game,

    "open_book": open_book,
    "write_book": write_book,

    "activate_cerberus": activate_cerberus  # Это пасхалка. Никаких поврежденных файлов нет.
}
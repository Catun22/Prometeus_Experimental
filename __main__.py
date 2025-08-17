"""
Точка входа в проект Prometheus.

Назначение:
    - Инициализирует приложение
    - Настраивает меню
    - Запускает главный цикл программы
"""

from core.menu import Menu, MenuStructure  # MenuStructure для аннотации
from core.lib.actions import ACTIONS
from core.lib.prompts import Prompts
from core.utilits.cleaner import clean
from core.utilits.installer import install


def main():
    """Основная функция."""
    action = ACTIONS
    # menu_structure можно спрятать в другом файле .py или .json.
    # Для наглядности оставил тут.
    menu_structure: MenuStructure = {
        "Работать": {
            "Учиться": {
                "Учить программирование": {
                    "Python": {
                        "Создать тему": "create_topic",
                        "Создать библиотеку": "create_library",
                    },
                    "JS": {"Создать тему": "create_js_topic"},
                    "HTML": {"Создать тему": "create_html_topic"},
                    "CSS": {"Создать тему": "create_css_topic"},
                },
                "Учить языки": {
                    "Английский": "learn_english",
                    "Французский": "learn_french",
                    "Немецкий": "learn_german",
                    "Испанский": "learn_spanish",
                },
            }
        },
        "Отдыхать": {
            "Смотреть фильм": "watch_movie",
            "Слушать музыку": "listen_music",
            "Играть": "play_game",
            "Читать книгу": {
                "Открыть книгу": "open_book",
                "Написать рецензию": "write_book",
            },
        },
        "Vk@lю4u;т%ь Cєr#+βє-яυ$?":{
            "Поврежденный фаа--+^ааа$%@__+*":"activate_cerberus"
        }
    }

    clean()  # Чистит терминал
    install()  # Установка colorama для Windows при необходимости (можно убрать)
    clean()

    print(Prompts.welcome)  # Приветствие пользователя

    # Вызываем меню
    menu = Menu("  МЕНЮ", menu_structure, action)
    menu.start()


if __name__ == "__main__":
    main()

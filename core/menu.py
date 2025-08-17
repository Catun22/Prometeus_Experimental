""" Модуль menu.py

    Содержит основной класс `class Menu`.

"""
from typing import Optional, Callable, Union, Dict, TypeAlias

from core.lib.prompts import MenuPrompts
from core.lib.prompts import Prompts
from core.ANSI.ANSI import FG, FG_BRIGHT, EFFECT

MenuStructure: TypeAlias = Dict[str, Union[str, "MenuStructure"]]  # Штука, которая делает аннотацию. 
# Меню содержит так называемый "рекурсивный словарь" - словарь в словаре, в котором ещё словарь, словарь, словарь...
# Интерпретатор будет "ходить" по словарям, как "по ветаям", до тех пор,
#  пока в конце не интерпретатор не наткнётся на заглушку или на какое-нибудь действие
# (вернее сказать на ссылку, которая подвязана к функции.
# (Если говорить очень просто, то пока интерпретатор не натнётся на имя функции. Мы проверим её наличие и попытаемся вызвать
# с помощью () таких скобок (ну или через .__call__() )).
# К слову, для этого из typing импортирован класс Callable (вызываемый), также для аннотации

class Menu:
    def __init__(self, title: Optional[str] = None, structure: MenuStructure | None = None, actions: Optional[dict[str, Callable[[], None]]] = None) -> None:
        """
        - `title` - аргумент, принимающий имя главного меню.

        - `structure` - аргумент, принимающий словари.
        """
        # Отдельная аннотация для наглядности
        self.__structure: MenuStructure
        self.__stack: list[MenuStructure]
        
        self.__title = title if title is not None else "Имя меню"
        self.__structure = structure if structure is not None else {"Пункт 1": {},"Пункт 2": {},"Пункт 3": {}}
        self.__stack = [self.__structure]  # для перехода "назад"
        self.__actions: dict[str, Callable[[], None]] = actions or {}
        # self.stack будет хранить "историю" тех пунктов, которые мы выбрали.
        # Благодаря этой штуке мы можем "возвращаться назад".
    
    def __container(self) -> None:
        """Содержит и хранит главный цикл меню"""
        while self.__stack:
            self.__current = self.__stack[-1]  # Текущее меню
            options = list(self.__current.keys())  # Список
            self.__display_menu(self.__title, options)  # Функция, отоброжающая меню
            
            print(MenuPrompts.choise)

            choice = input(Prompts.arrows)  # Сразу, чтобы не писать input в скрипте.
            exit_flag = self.__choice_handler(options, choice)  # Вернётся True, если "Выход"
            if exit_flag:  # Прерываем цикл
                break

    def __get_choice(self, choice: str) -> Optional[int]:
        """Проверка корректности ввода"""
        if not choice.isdigit():
            return None
        index = int(choice)
        if not (1 <= index <= len(self.__current) + 2):
            return None
        return index

    def __choice_handler(self, options: list[str], choice: str) -> bool:
        """
        Обработка выбора пользователя. 
        
        Возвращает `True` при выходе
        """
        
        index = self.__get_choice(choice)
        if index is None:
            print(MenuPrompts.bad_entry)
            return False  # Некорректный ввод, цикл продолжается

        if index == len(options) + 1:  # Если назад:
            if len(self.__stack) > 1:  # Если длина списка больше чем 1, (но не равна 1)
                self.__stack.pop()
            else:  # То мы в гланом меню, продолжаем цикл
                print(MenuPrompts.main_menu)
            return False
        elif index == len(options) + 2:  # Выход - возвращем True, цикл рвётся
            print(MenuPrompts.exit)
            return True
        else:  # В иных случаях (при выборе другого меню или действия/заглушки)
            selected = options[index - 1]  # Координируем индексы, чтобы был выбран верный вариант, а не на +1
            sub = self.__current[selected]  # В словаре находим ключ с именем selected
            if isinstance(sub, dict):  # Если там внутри словарь:
                self.__stack.append(sub)  # Добаляем в список выбранное
             # Если внутри ключ - строка, а !!значение!! - !!ссылка на функцию!!
            else:
                action = self.__actions.get(sub)
                if action:  # Выполняем действие
                    action()
                else:  # Если там ни словарь, ни функция, а заглушка
                    print(f"{MenuPrompts.perform_action} {selected}")
            return False  # Продолжаем цикл

    def __display_menu(self, title: str, structure: list[str]) -> None:
        """Отрисовывает меню из списка"""
        # Сюда был вынуждено добавлен модуль для раскраски меню
        # Так как эти пункты (кроме, естественно "Назад" и "Выход")
        # динамические, и невозможно создать для каждого пункта свой промпт и раскрасить.
        # Однако промпты для "Назад" и "Выход" были оставлены и они до сих пор имеют возможность
        # для изменения своей темы.
        # Сами промпты и задумывались для того, чтобы можно было поменять тему в любую секунду, 
        # не влезая в сам код и print.
        # Этот метод - единственное исключение.
        print(f"\n{title} "+ FG_BRIGHT.yellow + EFFECT.bold )  # Отрисуем титульник
        for number, item in enumerate(structure, 1):  # Нумеруем
            print(f"{number}. ", end="")
            print(f"{item}" + FG.green + EFFECT.bold)   
                   # И отрисуем
        
        # "Назад" и "Выход" добаляем как в самом конце всегда
        print(f"{len(structure) + 1}. {MenuPrompts.back}")
        print(f"{len(structure) + 2}. {MenuPrompts.exit}")
        
    def start(self) -> None:
        """Запускает меню"""
        self.__container()
  
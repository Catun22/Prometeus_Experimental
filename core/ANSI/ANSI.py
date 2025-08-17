"""ANSI.py

Позволяет раскрасить текст в терминале.
"""
# Я оставил всё так, как было в лекциях.
# Оставил лишь комментарии для себя, когда изучал это.


__fg = {
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "white": "37"
}

__bg = {
    "black": "40",
    "red": "41",
    "green": "42",
    "yellow": "43",
    "blue": "44",
    "magenta": "45",
    "cyan": "46",
    "white": "47"
}

__fgbright = {
    "black": "90",
    "red": "91",
    "green": "92",
    "yellow": "93",
    "blue": "94",
    "magenta": "95",
    "cyan": "96",
    "white": "97"
}

__bgbright = {
    "black": "100",
    "red": "101",
    "green": "102",
    "yellow": "103",
    "blue": "104",
    "magenta": "105",
    "cyan": "106",
    "white": "107"
}

__effects = {
    "reset": "0",           # Сброс всех эффектов
    "bold": "1",            # Жирный текст
    "underline": "4",       # Подчёркивание
    "blink": "5",           # Мигание (медленное)
    "reverse": "7",         # Инверсия цветов
    "hidden": "8",          # Скрытый текст
}


class ANSI_Code:
    # Создаем переменные класса
    # Они никогда не меняются
    __start = "\033["
    __end = "\033[0m"

    def __init__(self, code: str) -> None:
        self.__code = int(code).__str__()

    def __stock(self, obj: str) -> str:
        # Дополнительный класс, который используется в add и radd
        # \033[ + код (число, которое есть в нашем модуле) + "m" (обязательно) + ТЕКСТ + \033[0m
        return self.__start + self.__code + "m" + obj + self.__end

    def __exists(self, obj: str) -> str:
        # Меням просто "m" на ";наш кодm" один раз
        return obj.replace("m", f";{self.__code}m", count=1)

    def __add__(self, obj: object) -> object:
        if isinstance(obj, str):  # Если наш объект - строка: 
            return self.__stock(obj)
        return NotImplemented  # В иных случаях "не реализовано"

    def __radd__(self, obj: object) -> object:
        if isinstance(obj, str) and self.__start in obj:  # Если строка и есть \033[
            return self.__exists(obj)  # Возвращаем строку, у которой уже было форматирование
        elif isinstance(obj, str):  # Если операнд "пустой"
            return self.__stock(obj)  # Возвращаем только что отформатированную строку
        return NotImplemented  # В иных случаях "не реализовано"


# Классы как своеобразные контейнеры (хранилища)
class __FG:
    black: ANSI_Code
    red: ANSI_Code
    green: ANSI_Code
    yellow: ANSI_Code
    blue: ANSI_Code
    magenta: ANSI_Code
    cyan: ANSI_Code
    white: ANSI_Code


class __BG:
    black: ANSI_Code
    red: ANSI_Code
    green: ANSI_Code
    yellow: ANSI_Code
    blue: ANSI_Code
    magenta: ANSI_Code
    cyan: ANSI_Code
    white: ANSI_Code


class __FG_Bright:
    black: ANSI_Code
    red: ANSI_Code
    green: ANSI_Code
    yellow: ANSI_Code
    blue: ANSI_Code
    magenta: ANSI_Code
    cyan: ANSI_Code
    white: ANSI_Code


class __BG_Bright:
    black: ANSI_Code
    red: ANSI_Code
    green: ANSI_Code
    yellow: ANSI_Code
    blue: ANSI_Code
    magenta: ANSI_Code
    cyan: ANSI_Code
    white: ANSI_Code


class __Effect:
    reset: ANSI_Code           # Сброс всех эффектов
    bold: ANSI_Code            # Жирный текст
    underline: ANSI_Code       # Подчёркивание
    blink: ANSI_Code           # Мерцание (поддержка зависит от терминала)
    reverse: ANSI_Code         # Инверсия цветов
    hidden: ANSI_Code


# Циклы. Динамическое добавление
for key in __fg:  # Для ключа в словаре __fg (вверху)
    # Добавить в класс __FG, атрибут с именем key
    # и выражением (значением) экземпляра ANSI_Code, аргументом которого
    # является значение в словаре __fg, который мы находим по ключу key
    setattr(__FG, key, ANSI_Code(__fg[key]))
for key in __bg:
    setattr(__BG, key, ANSI_Code(__bg[key]))
for key in __fgbright:
    setattr(__FG_Bright, key, ANSI_Code(__fgbright[key]))
for key in __bgbright:
    setattr(__BG_Bright, key, ANSI_Code(__bgbright[key]))
for key in __effects:
    setattr(__Effect, key, ANSI_Code(__effects[key]))


# Создаем экземпляры, чтобы импортировалась как-бы "константная переменная"
FG: __FG = __FG()
BG: __BG = __BG()
FG_BRIGHT: __FG_Bright = __FG_Bright()
BG_BRIGHT: __BG_Bright = __BG_Bright()
EFFECT: __Effect = __Effect()

# Программа по поиску файлов

# Если увидите print("\033[92mКакая-то строка\033[0m)
# то это ANSI Escape Codes (Управлающие символы). Меняет цвет строки, делает жирным и тд.
# https://en.wikipedia.org/wiki/ANSI_escape_code

# Импортирую модули
import os
import time
# Создаю главную функцию
def findler() -> None:
# Создаю пустой список, в который добавлю кортежи из двух элементов
    base_path: list[tuple[str, int]] = []
# Вызываю функции. Пометил цифрами, чтобы было видно где какая
    welcome() # 1
    pattern = enter() # 2
    start = time.time() # Тут начинаем отсчёт работы программы
    search_files(base_path, pattern) # 3
    choosed = choise() # 4
    save_to_file(base_path, choosed) # 5
# Тут мои созданные фунеции заканчиваются
    end = time.time() # Время, когда все функции прекратили работу
    print("\033[92mEverything is saved in a file: saved_path.txt\033[0m")
# Расчитываем время работы программы (именно самого расчёта), а не с момента запуска
    timer = round(end - start, 2)
    print(f"\033[92mThe program is completed in {timer} seconds!\033[0m")

# Приветствие для пользователя
def welcome(): # 1
    print("\n\t_____________(ﾉಥ益ಥ)ﾉ______________")
    print("\033[32m\tWelcome to the file search program!\033[0m")
    print("\t___________________________________\n")
# Пользователь вводит название файла для поиска
# Или нажимает Enter для поиска README по умолчанию
def enter(): # 2
    prompt = "Enter the name of the file to search for, or by default \033[33mREADME\033[0m\n>> "
    return (input(prompt) or "README").lower().strip() # В нижний регистр и без пробелов. Возврат
    # не создаю следующего вида код: x = int(inpit("Что-то")), а сразу пишу к return для экономии кода

# Функция, которая ищет файл. Аргументы: пустой список и название файла из функции enter
def search_files(base_path: list[tuple[str, int]], pattern: str) -> None: # 3
    # Далее как в лекции, только без count. Счёт будет вестись по-другому методу
    for path, _ , files in os.walk("/"): # "_" вместо dirs. Не используется
        for file in files:
            if pattern in file.lower():
                # полный путь в переменную для удобства
                full_path = os.path.join(path, file)
                # проверка на линки
                if os.path.islink(full_path):
                    continue # Тут заканчивается то, что было в лекции
            # добавляем к пустому списку путь и размер
                size = os.path.getsize(full_path) # запрашиваем размер файла по пути
# base_path - список, в котором кортежи из двух значений full_path и size
                base_path.append((full_path, size))

def choise(): # 4
    prompt = "Select the displayed size:\033[32m\n1 - KB\n2 - MB\n3 - GB\033[0m"
    print(prompt)
    # Бесконечный цикл с проверкой на валидность
    # Вместо цифр можно написать другую проверку, например KB, MB, GB
    while True:
        try:
            enter = int(input("Please, Enter\n>> "))
            if enter >= 1 and enter <= 3:
                return enter # Возвращаю значение
            else:
                print("Number must be 1, 2 or 3.")
        except ValueError:
            print("Enter a valid number: 1, 2 or 3")

# Функция для сохранения пути в файл
def save_to_file(base_path: list[tuple[str, int]], choosed: int) -> None: # 5
    # Создаю два словаря со значениями и единицами измерения. Словарь (dict) - изменяемый, контейнерный тип данных. Ключ: значение
    scale = {1: 1024, 2: 1024**2, 3: 1024**3}
    units = {1: "KB", 2: "MB", 3: "GB"}
    # Анонимная функция для сортировки. Благодаря ей - меньше кода
    base_path.sort(key=lambda x: x[1], reverse=False) # Мы вызываем метод sort, поэтому можно менять сортировку. Как в лекциях. Специально оставил reverse
    # Менеджер контекста для работы с файлами. Сразу закрывает файл
    with open("saved_path.txt", "w", encoding="utf-8") as f: # Задаю кодировку UTF-8. w - перезаписывать файл и f -  переменная
        # Распаковываю base_path, в котором хранится путь и размер (напоминаю, что это список внутри которого кортежи, в которых в свою очередь 2 элемента)
        for path, size in base_path:
            total_size = round(size / scale[choosed], 2) # Сюда пишу размер из функции choise и округляю
            # Метод для записи строки в файл
            f.write(f"{path} — {total_size} {units[choosed]}\n") # Путь - (тире) размер и обозначение величины - так будет в файле
    print(f"\033[92mIt's done! Files found: {len(base_path)}\033[0m")

# Для импорта
if __name__ == "__main__":
    findler() # Вызов главной функции

# Что можно добавить?
# Модуль colorama - чтобы работать с модулем, а не символами
# pip install colorama
# Проверку, если ничего не найдено
# Выбор директории пользователем
# Добавить GUI. Например, tkinter/customtkinter,PyQt5/PyQt6, PySide6, Kivy или другие
# Вместо .txt экспортировать в .csv (Excel)
# Фильтра не по размеру, а, например, дате/расширению

# А вообще, благодаря сортировке по размеру файла
# можно находить "тяжеловесные", ненужные файлы и удалять их,
# либо находить "маловесные" подозрительные файлы,
# особенно с необычным названием в виде символов,
# и отправлять их на проверку антивирусу.
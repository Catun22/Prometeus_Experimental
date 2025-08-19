"""installer.py 

Позволяет установить colorama для Windows.
"""
import sys
import ctypes


def ansi_code_fixer() -> None:
    """Позволяет отоброжать ANSI последовательности через системные ресурсы Windows API"""
    # Загружаем библиотеку kernel32.dll (Windows API)
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    
    # Константы Windows API
    STD_OUTPUT_HANDLE = -11  # Дескриптор стандартного вывода
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004  # Флаг для включения ANSI escape-последовательностей
    
    # Явно задаём сигнатуры функций
    kernel32.GetStdHandle.argtypes = [ctypes.c_ulong]
    kernel32.GetStdHandle.restype = ctypes.c_void_p
    
    kernel32.GetConsoleMode.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
    kernel32.GetConsoleMode.restype = ctypes.c_int
    
    kernel32.SetConsoleMode.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
    kernel32.SetConsoleMode.restype = ctypes.c_int
    
    # Проверяем версию Windows
    if sys.platform == "win32":
        ver = sys.getwindowsversion()
        # major=10, build>=10586 → поддержка ANSI есть
        if ver.major > 10 or (ver.major == 10 and ver.build >= 10586):
            # Получаем дескриптор стандартного вывода
            handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    
            if handle == ctypes.c_void_p(-1).value:  # INVALID_HANDLE_VALUE = -1
                raise ctypes.WinError(ctypes.get_last_error())
    
            # Получаем текущий режим консоли
            mode = ctypes.c_ulong()
            if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                raise ctypes.WinError(ctypes.get_last_error())
    
            # Добавляем флаг ANSI
            new_mode = mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
            if not kernel32.SetConsoleMode(handle, new_mode):
                raise ctypes.WinError(ctypes.get_last_error())
    
            print("Поддержка ANSI escape включена.")
        else:
            print("Ваша версия Windows слишком старая, ANSI escape-последовательности не поддерживаются.")
    # Тест: раскрашенный вывод
    print("\033[31mКрасный текст\033[0m и \033[32mзелёный текст\033[0m")


def install() -> None:
    """Устанавливает библиотку colorama"""

    prompt = (
    "Библиотека colorama не установлена.\n"
    "Используем встроенный механизм системы ctypes для поддержания ANSI escape code.\n"
    )
    try:  # Пытаемся вызвать функцию, ремонтирующую терминал Win, для отображения цветов
        from colorama import just_fix_windows_console
        just_fix_windows_console()
    except ImportError:  # Ловим ошибки при импорте - если ошибка есть, значит colorama нет
        print(prompt)
        if sys.platform == "win32":
            ansi_code_fixer()

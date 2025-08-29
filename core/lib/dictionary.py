"""
Содержит интерактивный языковой словарь.

Может добавлять языки в .md файл, перевод, транскрипцию и контекст (предложения с использованием слова).

В программе существует "поддержка" русского, английского, немецкого, французского, испанского языков.

Словарь позволяет добавить любое количество языков и слов.

Имеет возможность добавления, поиска, редактирования и изменения слов, переводов, транскрипций.

Этот модуль можно использовать интерактивно через основную программу или "напрямую", работая с классами, приведенными в модуле.
"""
import os
from typing import Dict, List, Optional, Any

from rich.console import Console
from rich.text import Text
from rich.markdown import Markdown

from core.lib.prompts import Prompts, PromptsDict, support_color

class Word:
    def __init__(self, base: str) -> None:
        """Создает объект с основным словом, переводами, транскрипцией и контекстом"""
        self.base = base  # Поле с основным словом. То есть на русском, если родной русский
        self.translations: Dict[str, str] = {}  # Словарь с переводом
        self.transcriptions: Dict[str, str] = {} # Словарь с транскрипцией
        self.contexts: List[str] = []  # Список с контекстом (просто предложения с вашим словом)

    def add_translation(self, lang: str, word: str) -> None:
        """Добавить перевод в словарь. Язык - ключ, значение - перевод"""
        self.translations[lang] = word

    def add_transcription(self, lang: str, transcription: str) -> None:
        """Добавить транскрипцию в словарь. Язык - ключ, значение - транскрипция"""
        self.transcriptions[lang] = transcription
    
    def add_context(self, sentence: str) -> None:
        """Добавить транскрипцию в список. Просто добавляем аргумент в список"""
        self.contexts.append(sentence)
        
    def remove_translation(self, lang: str) -> None:
        """Удаляет перевод"""
        if lang in self.translations:  # Если ключ есть в словаре (язык - ключ)
            del self.translations[lang]  # Удалить значение перевода с таким ключом
            
    def remove_transcription(self, lang: str) -> None:
        """Удаляет транскрипцию"""
        if lang in self.transcriptions: # Если ключ есть в словаре (язык - ключ)
            del self.transcriptions[lang] # Удалить значение транскрипции с таким ключом
            
    def remove_context(self, index: int) -> None:
        """Удаляет контекст"""
        if 0 <= index < len(self.contexts):  # Если номер индекса контекста из списка больше или равен нулю,
            self.contexts.pop(index)  # Но меньше длины, то удалить список

    def __str__(self, show_context: bool = False) -> str:
        """Выводит результат"""
        lines = [f"Слово: {self.base}\n"]  # Список с основным словом
        # Получаем объединенный и отсортированный список всех языков из переводов и транскрипций
        langs = sorted(set(self.translations.keys()) | set(self.transcriptions.keys()))
        # Для каждого языка формируем строку с переводом и транскрипцией
        for lang in langs:
            # Получаем перевод для языка, если нет - используем "-"
            tr = self.translations.get(lang, "-")
            # Получаем транскрипцию для языка, если нет - используем "-"
            ts = self.transcriptions.get(lang, "-")
            # Формируем строку в формате Markdown и добавляем в список
            lines.append(f">**{lang}**: *{tr}* `[{ts}]`\n")

        # Если нужно показать контекст и контексты существуют (аргумент)
        if show_context and self.contexts:  # Если мы не удалили его через remove_context или не добавили
            # Добавляем заголовок для раздела контекста
            lines.append(">**Контекст**:")
            # Добавляем каждый контекст как элемент списка
            for ctx in self.contexts:
                lines.append(f"> - {ctx}")
            # Добавляем пустую строку для разделения
            lines.append("")
        # Объединяем все строки списка в одну строку с переносами
        return "\n".join(lines)


class Dictionary:
    def __init__(self) -> None:
        self.console = Console()
        self.words: Dict[str, Word] = {}  # Ключ - базовое слово, значение объект Word
        self.filename: Optional[str] = None  # Путь к файлу словаря

    def load_from_md(self, filename: str) -> None:
        """Загружает слова из markdown-файла"""
        self.filename = filename
        if not os.path.exists(filename):
            return

        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        word: Word | None = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith("Слово:"):
                base = line[len("Слово:"):].strip()
                if base:
                    word = Word(base)
                    self.words[base] = word
                else:
                    word = None

            elif word and line.startswith(">**") and "**:" in line and "`[" in line:
                try:
                    lang = line.split("**")[1].split(":")[0].strip()
                    translation = line.split("*")[1].strip()
                    transcription = line.split("`[")[1].split("]`")[0].strip()
                    word.add_translation(lang, translation)
                    word.add_transcription(lang, transcription)
                except IndexError:
                    continue
            # Контекст
            elif word and line.startswith("> - "):
                context = line[4:].strip()
                word.add_context(context)


    def word_exists(self, word: Word) -> bool:
        """Проверяет существование слова"""
        # Проверяем, существует ли слово в словаре по ключу (base)
        return word.base in self.words

    def add_word(self, word: Word) -> None:
        """Добавляет слово в словарь"""
        # Если слова нет в словаре, добавляем его
        if not self.word_exists(word):
            self.words[word.base] = word
            self.console.print(f"{PromptsDict.word} '{word.base}' {PromptsDict.added}")
        else:
            self.console.print(f"{PromptsDict.word} '{word.base}' {PromptsDict.already_have}")

    def remove_word(self, base: str) -> bool:
        """Удаляет слово из словаря"""
        # Если слово существует в словаре
        if base in self.words:
            # Удаляем слово из словаря
            del self.words[base]
            self.console.print(PromptsDict.word + Text(f" '{base}' ") + PromptsDict.deleted)
            return True
        # Если не существует
        else:
            self.console.print(PromptsDict.word + Text(f" '{base}' ") + PromptsDict.no_found)
            return False

    def edit_word(self, base: str, **kwargs: Any) -> bool:
        """Изменяет слово"""
        # Если слова нет в словаре, выходим
        if base not in self.words:
            
            self.console.print(PromptsDict.word + Text(f" '{base}' ") + PromptsDict.no_found)
            return False  # И возвращаем False
        
        # Получаем объект слова
        word = self.words[base]
        
        # Если передан новый base
        if 'new_base' in kwargs:
            new_base = kwargs['new_base']
            # Если новый base отличается от текущего и уже существует
            if new_base != base and new_base in self.words:
                self.console.print(PromptsDict.word  + Text(f" '{new_base}' ") + PromptsDict.exists)
                return False
                
            # Обновляем ключ в словаре
            if new_base != base:
                if not isinstance(new_base, str):
                    self.console.print(PromptsDict.must_be_str)
                    return False
                self.words[new_base] = self.words.pop(base)
                word.base = new_base
        
        # Если передан перевод
        if 'translation' in kwargs:
            lang, trans = kwargs['translation']
            word.add_translation(lang, trans)
        
        # Если передана транскрипция
        if 'transcription' in kwargs:
            lang, transcr = kwargs['transcription']
            word.add_transcription(lang, transcr)
        
         # Если нужно добавить контекст
        if 'add_context' in kwargs:
            word.add_context(kwargs['add_context'])
        
        # Если нужно удалить контекст
        if 'remove_context' in kwargs:
            index = kwargs['remove_context']
            word.remove_context(index)
            
        self.console.print(PromptsDict.word + Text(f" '{base}' ") + PromptsDict.edited)
        return True

    def save_to_md(self, filename: Optional[str] = None, show_context: bool = False) -> None:
        """Сохраняет словарь в файл"""
        # Если имя файла не указано, используем сохраненное
        if filename is None:
            if self.filename is None:
                self.console.print(PromptsDict.no_file_save)
                return
            filename = self.filename
        
        # Создаём папки, если их нет
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # Полностью перезаписываем файл
        with open(filename, "w", encoding="utf-8") as f:
            # Для каждого слова в словаре
            for word in self.words.values():
                # Преобразуем слово в строку и записываем в файл
                f.write(word.__str__(show_context=show_context) + "\n\n")
                
        self.console.print(PromptsDict.saved_dict, f"{filename}")

    def find(self, query: str) -> List[Word]:
        """Ищет схожие слова"""
        results: List[Word] = []
        # Приводим запрос к нижнему регистру
        queries = query.lower().split()
        
        # Для каждого слова в словаре
        for word in self.words.values():
            # Если запрос содержится в базовом слове или в любом из переводов
            if any(q in word.base.lower() or any(q in trans.lower() for trans in word.translations.values()) for q in queries):
                # Добавляем слово в результаты
                results.append(word)
                
        return results
        
    def find_exact(self, query: str) -> Optional[Word]:
        """Ищет точные совпадения"""
        # Приводим запрос к нижнему регистру
        query = query.lower()
        # Для каждого слова в словаре
        for word in self.words.values():
            # Если запрос точно совпадает с базовым словом или с любым из переводов
            if (query == word.base.lower() or 
                any(query == trans.lower() for trans in word.translations.values())):
                 # Возвращаем найденное слово
                return word
        # Если ничего не найдено, возвращаем None
        return None
        
    def list_words(self, limit: int = 20, offset: int = 0) -> List[Word]:
        # Преобразуем значения словаря в список
        words = list(self.words.values())
        return words[offset:offset+limit]
        
    def count_words(self) -> int:
        """Возвращает количество слов в словаре"""
        return len(self.words)


def interactive_mode(dictionary: Dictionary) -> None:
    """Интерактивный режим для работы со словарем"""
    console = Console()
    while True:
        print("\n")
        show_main_menu(console)
        choice = console.input(Prompts.arrows).strip()
        
        if choice == "1":
            add_word(console, dictionary)
        elif choice == "2":
            find_exact_word(console, dictionary)
        elif choice == "3":
            edit_word(console, dictionary)
        elif choice == "4":
            delete_word(console, dictionary)
        elif choice == "5":
            show_words(console, dictionary)
        elif choice == "6":
            save_words(dictionary)
        elif choice == "7":
            if exit(console, dictionary):
                break
        else:
            console.print(PromptsDict.wrong_choose)


def show_main_menu(console: Console) -> None:
    """Показывает главное меню словаря"""
    console.print(PromptsDict.mode_interactive)
    console.print(Text("1. ", style=support_color) + PromptsDict.add_word)
    console.print(Text("2. ", style=support_color) + PromptsDict.find_word)
    console.print(Text("3. ", style=support_color) + PromptsDict.edit_word)
    console.print(Text("4. ", style=support_color) + PromptsDict.delete_word)
    console.print(Text("5. ", style=support_color) + PromptsDict.show_word)
    console.print(Text("6. ", style=support_color) + PromptsDict.save_word)
    console.print(Text("7. ", style=support_color) + PromptsDict.exit_word)
    console.print("\n", PromptsDict.choose_word)


def add_word(console: Console, dictionary: Dictionary) -> None:
    """Добавляет базовое слово"""
    console.print(PromptsDict.enter_word)
    base = console.input(Prompts.arrows).strip()
    if not base:
        console.print(PromptsDict.word_no_space)
        return
        
    word = Word(base)
    add_translations_and_transcriptions(console, word)
    add_contexts(console, word)
    dictionary.add_word(word)


def add_translations_and_transcriptions(console: Console, word: Word) -> None:
    """Добавляет перевод и транскрипцию"""
    while True:
        console.print(PromptsDict.enter_language)
        lang = console.input(Prompts.arrows).strip()
        if lang.lower() == 'стоп':
            break
        
        console.print(PromptsDict.enter_translate)
        translation = console.input(Prompts.arrows).strip()
        console.print(PromptsDict.enter_transcript)
        transcription = console.input(Prompts.arrows).strip()
        
        if translation:
            word.add_translation(lang, translation)
        if transcription:
            word.add_transcription(lang, transcription)


def add_contexts(console: Console, word: Word) -> None:
    """Добаляет контекст"""
    while True:
        console.print(PromptsDict.enter_context)
        context = console.input(Prompts.arrows).strip()
        if context.lower() == 'стоп':
            break
        if context:
            word.add_context(context)


def find_exact_word(console: Console, dictionary: Dictionary) -> None:
    """Ищет слова с точным совпадением"""
    console.print(PromptsDict.enter_word_to_find)
    query = console.input(Prompts.arrows).strip()
    if not query:
        console.print(PromptsDict.ask_no_space)
        return
        
    exact_match = dictionary.find_exact(query)
    if exact_match:
        console.print(f"\n{PromptsDict.exactly_find}")
        md = Markdown(exact_match.__str__(show_context=True))
        console.print(md)
    else:
        find_word(console, dictionary, query)


def find_word(console: Console, dictionary: Dictionary, query: str) -> None:
    """Ищет слова с частичным совпадением"""
    results = dictionary.find(query)
    if results:
        console.print(f"\n{PromptsDict.count} {len(results)}")
        for i, word in enumerate(results, 1):
            console.print(f"{i}. {word.base}")
        
        console.print(PromptsDict.look_or_back)
        view_index = console.input(Prompts.arrows).strip()
        if view_index.isdigit() and 1 <= int(view_index) <= len(results):
            md = Markdown(results[int(view_index)-1].__str__(show_context=True))
            console.print(md)
    else:
        console.print(PromptsDict.no_matches)


def edit_word(console: Console, dictionary: Dictionary) -> None:
    """Изменяет слово"""
    console.print(PromptsDict.enter_to_edit)
    base = console.input(Prompts.arrows).strip()
    if not base:
        console.print(PromptsDict.word_no_space)
        return
        
    if base not in dictionary.words:
        console.print(PromptsDict.not_found_in_dict)
        return
        
    word = dictionary.words[base]
    console.print(PromptsDict.current_data)
    md = Markdown(word.__str__(show_context=True))
    console.print(md)
    
    console.print("\n", PromptsDict.want_to_change)
    show_edit_menu(console)
    edit_choice = console.input(Prompts.arrows).strip()
    get_edit_choice(console, dictionary, base, word, edit_choice)


def show_edit_menu(console: Console) -> None:
    """Отображает меню для изменения слова"""
    console.print(Text("1. ", style=support_color) + PromptsDict.add_word)
    console.print(Text("2. ", style=support_color) + PromptsDict.edit_translate)
    console.print(Text("3. ", style=support_color) + PromptsDict.edit_transcript)
    console.print(Text("4. ", style=support_color) + PromptsDict.edit_context)
    console.print(Text("5. ", style=support_color) + PromptsDict.delete_context)
    console.print(PromptsDict.choose_action)


def get_edit_choice(console: Console, dictionary: Dictionary, base: str, word: Word, edit_choice: str) -> None:
    """Выполняет действе в зависимости от выбора"""
    if edit_choice == "1":
        console.print(PromptsDict.new_base)
        new_base = console.input(Prompts.arrows).strip()
        if new_base:
            dictionary.edit_word(base, new_base=new_base)
            
    elif edit_choice == "2":
        console.print(PromptsDict.new_language)
        lang = console.input(Prompts.arrows).strip()
        console.print(PromptsDict.enter_translate)
        translation = console.input(Prompts.arrows).strip()
        if lang and translation:
            dictionary.edit_word(base, translation=(lang, translation))
            
    elif edit_choice == "3":
        console.print(PromptsDict.new_language)
        lang = console.input(Prompts.arrows).strip()
        console.print(PromptsDict.new_enter_transcript)
        transcription = console.input(Prompts.arrows).strip()
        if lang and transcription:
            dictionary.edit_word(base, transcription=(lang, transcription))
            
    elif edit_choice == "4":
        console.print(PromptsDict.new_enter_context)
        context = console.input(Prompts.arrows).strip()
        if context:
            dictionary.edit_word(base, add_context=context)
            
    elif edit_choice == "5":
        console.print(PromptsDict.current_context)
        for i, ctx in enumerate(word.contexts):
            console.print(f"{i+1}. {ctx}")
        
        console.print(PromptsDict.number_context_delete)
        index_str = console.input(Prompts.arrows).strip()
        if index_str.isdigit():
            index = int(index_str) - 1
            dictionary.edit_word(base, remove_context=index)


def delete_word(console: Console, dictionary: Dictionary) -> None:
    """Удаляет слово"""
    console.print(PromptsDict.word_to_delete)
    base = console.input(Prompts.arrows).strip()
    if base:
        dictionary.remove_word(base)


def show_words(console: Console, dictionary: Dictionary) -> None:
    """Показывает слова в словаре"""
    limit = 10
    page = 0
    total = dictionary.count_words()
    
    while True:
        words = dictionary.list_words(limit=limit, offset=page*limit)
        print("\n")
        console.print(PromptsDict.page + Text(f"{page+1}") + PromptsDict.all_words + Text(f"{total}") + ":")
        for i, word in enumerate(words, 1):
            print(f"{page*limit + i}. {word.base}")

        if page*limit + limit < total:
            line = Text("\n'n' ") + PromptsDict.next_page + Text(", 'p' ") + PromptsDict.back_page + Text(", 'q' ") + PromptsDict.exit_page
            console.print(line)
        else:
            line = Text("\n'p' ") + PromptsDict.back_page + Text(", 'q' ") + PromptsDict.exit_page
            console.print(line)

        nav = console.input(Prompts.arrows).strip().lower()
        if nav == 'n' and page*limit + limit < total:
            page += 1
        elif nav == 'p' and page > 0:
            page -= 1
        elif nav == 'q':
            break


def save_words(dictionary: Dictionary) -> None:
    """Сохраняет слова"""
    dictionary.save_to_md(show_context=True)


def exit(console: Console, dictionary: Dictionary) -> bool:
    """Сохранение перед выходом"""
    console.print(PromptsDict.save_edits)
    save = console.input(Prompts.arrows).strip().lower()
    if save == 'д':
        dictionary.save_to_md(show_context=True)
    return True

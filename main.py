import re
from typing import Dict, List, Tuple


def words_count(text: str, result: Dict[str, int]) -> Dict[str, int]:
    """
    Заполняет словарь частоты слов из строки текста.

    Args:
        text (str): строка текста для анализа.
        result (Dict[str, int]): существующий словарь частоты слов, который будет дополнен.

    Returns:
        Dict[str, int]: обновленный словарь частоты слов.
    """

    template = re.compile(r'[^\d,\W]+[-]?\w*')
    words = template.findall(text.lower())
    for word in words:
        if result.get(word):
            result[word] += 1
        else:
            result[word] = 1
    return result


def print_result(sorted_list: List, file=None) -> None:
    """
    Выводит в консоль или в файл результатов.

    Args:
        sorted_list (List): отсортированный список кортежей (слово, частота).
        file : если None, вывод происходит в консоль, иначе - в файл.
    """

    print(f'{"_" * 37}', file=file)
    print(f'|{"Слово":^25}| Частота |', file=file)
    print(f'|{"-" * 25}|{"-" * 9}|', file=file)
    for word in sorted_list:
        print(f'|{word[0]:^25}|{word[1]:^9}|', file=file)
    print(f'{"¯" * 37}', file=file)


def main_menu() -> Dict[str, int]:
    """
    Основное меню - выбор источника информации.

    Returns:
        Dict[str, int]: словарь из слов и их частоты из выбранного источника.
    """

    while True:
        print('Укажите источник текста:\n'
              '1 - Текстовый файл;\n'
              '2 - Ввод текста в консоль.')
        text_source = input('Ввод: ')

        if text_source == '1':
            return load_file()
        elif text_source == '2':
            return write_text()
        else:
            print('Неверно указан источник текста. Введите 1 или 2.')


def load_file() -> Dict[str, int]:
    """
    Загружает текст из файла и подсчитывает частоту слов.

    Returns:
        Dict[str, int]: словарь частоты слов из файла.
    """

    words = dict()
    my_file = r'C:\TextAnalyzer\my_text.txt'
    file_path = input('\nУкажите полный путь до файла: ')

    try:
        with open(my_file, 'r', encoding='utf-8') as file:
            for line in file:
                words = words_count(line, words)

        return words

    except (FileNotFoundError, FileExistsError):
        print('Неверно указан путь до файла или нет к нему доступа.')
        return load_file()


def write_text() -> Dict[str, int]:
    """
    Принимает текстовый ввод от пользователя для анализа частоты слов.

    Returns:
        Dict[str, int]: словарь из слов частоты слов из текста.
    """

    words = dict()
    original_text = input('\nВведите текст для анализа:\n')

    while not original_text:
        print('Текст не может быть пустым. Повторите ввод!')
        original_text = input('Введите текст для анализа:\n')

    words = words_count(original_text, words)
    return words


def selection_sorting() -> bool:
    """
    Меню выбора направления сортировки.

    Returns:
        bool: True для сортировки по убыванию, False для сортировки по возрастанию.
    """

    flag = None
    while True:
        print('\nВыберете сортировку слов по частоте:\n'
              '1 - По убыванию;\n'
              '2 - По возрастанию.')
        user_choice = input('Ввод: ')

        if user_choice == '1':
            flag = True
            break
        elif user_choice == '2':
            flag = False
            break
        else:
            print('Неверно выбрана сортировка. Введите 1 или 2.')

    return flag


words_dict = main_menu()

reverse_flag = selection_sorting()

sorted_words = sorted(words_dict.items(), key=lambda w: (w[1], w[0]), reverse=reverse_flag)

if len(words_dict) <= 500:
    print_result(sorted_words)
else:
    print('Количество слов превышает 500. Результат будет записан в файл "result.txt".')

with open('result.txt', 'w', encoding='utf-8') as file:
    print_result(sorted_words, file)


print('Общее количество слов:', sum(words_dict.values()))
# print('Топ-10 слов:')
# print(dict(sorted_words[:10]))
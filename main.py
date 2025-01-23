import re
from typing import Dict, List


def words_count(text: str, result: Dict[str, int], stop_words: List[str]) -> Dict[str, int]:
    """
    Заполняет словарь частоты слов из строки текста.

    Args:
        text (str): строка текста для анализа.
        result (Dict[str, int]): существующий словарь частоты слов, который будет дополнен.
        stop_words (List[str]): список стоп-слов.

    Returns:
        Dict[str, int]: обновленный словарь частоты слов.
    """

    template = re.compile(r'[^\d,\W]+[-]?\w*')
    words_line = template.findall(text.lower())

    for word in set(words_line):
        if word not in stop_words:
            if result.get(word):
                result[word] += words_line.count(word)
            else:
                result[word] = words_line.count(word)
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

    stop_words = fill_stop_words()

    while True:
        print('\nУкажите источник текста:\n'
              '\t1 - Текстовый файл;\n'
              '\t2 - Ввод текста в консоль.')
        text_source = input('Ввод: ')

        if text_source == '1':
            return load_file(stop_words)
        elif text_source == '2':
            return write_text(stop_words)
        else:
            print('Неверно указан источник текста. Введите 1 или 2.')


def fill_stop_words() -> List[str]:
    """
    Заполняет список со стоп-словами, если это необходимо.

    Returns:
        List[str]: список стоп-слов.
    """

    while True:
        print('Стоп-слова - слова, которые не будут учитываться при подсчете частоты слов.\n'
              '\t1 - Необходима фильтрация стоп-слов;\n'
              '\t0 - Фильтрация не нужна.')
        user_choice = input('Ввод: ')

        if user_choice == '0':
            return []

        elif user_choice == '1':
            while True:
                stop_words = input('Введите стоп-слова через пробел: ')

                control_check = re.findall(r'[^\d,\W]+[-]?\w*', stop_words)
                stop_words = stop_words.split()

                # сравниваем списки, чтобы убедиться, то пользователь не ввел посторонние символы
                if control_check == stop_words:
                    return stop_words
                else:
                    print('Ошибка ввода. В словах могут присутствовать только буквы и дефис("-").')

        else:
            print('Неверно сделан выбор. Введите 1 или 0.')


def load_file(stop_words: List[str]) -> Dict[str, int]:
    """
    Загружает текст из файла и подсчитывает частоту слов.

    Args:
        stop_words (List[str]): список стоп-слов.

    Returns:
        Dict[str, int]: словарь частоты слов из файла.
    """

    words = dict()
    my_file = r'C:\TextAnalyzer\allpart_238.txt'
    file_path = input('\nУкажите полный путь до файла: ')

    try:
        with open(my_file, 'r', encoding='utf-8') as file:
            for line in file:
                words = words_count(line, words, stop_words)

        return words

    except (FileNotFoundError, FileExistsError):
        print('Неверно указан путь до файла или нет к нему доступа.')
        return load_file(stop_words)


def write_text(stop_words: List[str]) -> Dict[str, int]:
    """
    Принимает текстовый ввод от пользователя для анализа частоты слов.

    Args:
        stop_words (List[str]): список стоп-слов.

    Returns:
        Dict[str, int]: словарь из слов частоты слов из текста.
    """

    words = dict()
    original_text = input('\nВведите текст для анализа:\n')

    while not original_text:
        print('Текст не может быть пустым. Повторите ввод!')
        original_text = input('Введите текст для анализа:\n')

    words = words_count(original_text, words, stop_words)
    return words


def selection_sorting() -> bool:
    """
    Меню выбора направления сортировки.

    Returns:
        bool: True для сортировки по убыванию, False для сортировки по возрастанию.
    """

    while True:
        print('\nВыберете сортировку слов по частоте:\n'
              '\t1 - По убыванию;\n'
              '\t2 - По возрастанию.')
        user_choice = input('Ввод: ')

        if user_choice == '1':
            flag = True
            return flag
        elif user_choice == '2':
            flag = False
            return flag
        else:
            print('Неверно выбрана сортировка. Введите 1 или 2.')


def top_words(words: List, reverse: bool) -> None:
    """
    Выводит топ-10 слов на экран.

    Args:
        words (List): отсортированный список кортежей (слово, частота).
        reverse (bool): показывает направление сортировки.
    """

    while True:
        print('\nКак поступить с топ-10 слов?\n'
              '\n1 - Показать на экране;'
              '\n2 - Не выводить.')
        user_choice = input('Ввод: ')

        if user_choice == '1':
            if reverse:
                top = words[:10]
            else:
                top = sorted(words[-11:], key=lambda w: (w[1], w[0]), reverse=True)

            print('Топ-10 слов:')
            print_result(top)
            break

        elif user_choice == '2':
            break
        print('Такого выбора нет. Введите 1 или 2.')


def frequency_thresholds(words: Dict[str, int]) -> List:
    """
    Фильтрует частотный словарь слов, исключая из него редко встречающиеся слова

    Args:
        words (Dict[str, int]): частотный словарь слов.

    Returns:
        List: отсортированный список кортежей (слово, частота).
    """
    while True:
        print('\nИсключение редко встречающихся слов (например, с частотой < N).\n'
              '\tЧисло N - Для исключения слов из списка с частотой N и меньше;\n'
              '\t0 - Если исключать слова из списка не нужно.')
        number_n = input('Введите N: ')

        if number_n.isdigit() and int(number_n) >= 0:
            number_n = int(number_n)
            filtered_list = list(words.items())

            if number_n > max(words.values()):
                print('Число N больше наибольшей частоты слов. Будет возвращен весь список')

            elif number_n > 0:
                filtered_list = list(filter(lambda x: x[1] > number_n, words.items()))
                return filtered_list

            return filtered_list

        else:
            print('Ошибка при вводе числа. Число должно быть больше или равно 0 и содержать исключительно цифры')


words_dict = main_menu()
filtered_words = frequency_thresholds(words_dict)
reverse_flag = selection_sorting()
# Если reverse_flag == True, то (-1)^1, т.е. сортировка производится по убыванию, иначе - по возрастанию
sorted_words = sorted(filtered_words, key=lambda w: ((-1) ** reverse_flag * w[1], w[0]))

if len(filtered_words) <= 500:
    print_result(sorted_words)
    print('Общее количество слов:', sum(words_dict.values()))
else:
    print('Количество слов превышает 500. Результат можете посмотреть в файле "result.txt".')

with open('result.txt', 'w', encoding='utf-8') as file:
    print_result(sorted_words, file=file)
    print(f'Общее количество слов: {sum(words_dict.values())}', file)

top_words(sorted_words, reverse_flag)

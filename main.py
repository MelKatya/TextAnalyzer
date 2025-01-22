import re
from typing import Dict, List, Tuple


def words_count(text: str, result: Dict[str, int], stop_words) -> Dict[str, int]:
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
        if word not in stop_words:
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

    stop_words = fill_stop_words()

    while True:
        print('Укажите источник текста:\n'
              '1 - Текстовый файл;\n'
              '2 - Ввод текста в консоль.')
        text_source = input('Ввод: ')

        if text_source == '1':
            return load_file(stop_words)
        elif text_source == '2':
            return write_text()
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
              '1 - если необходима фильтрация стоп-слов.\n'
              '0 - если фильтрация не нужна.')
        user_choice = input('Ввод: ')

        if user_choice == '0':
            return []

        elif user_choice == '1':
            while True:
                stop_words = input('Введите стоп-слова через пробел: ')

                control_check = re.findall(r'[^\d,\W]+[-]?\w*', stop_words)
                stop_words = stop_words.split()

                if control_check == stop_words:
                    return stop_words
                else:
                    print('Ошибка ввода. В словах могут присутствовать только буквы и дефис("-").')

        else:
            print('Неверно сделан выбор. Введите 1 или 0.')


def load_file(stop_words) -> Dict[str, int]:
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
                words = words_count(line, words, stop_words)

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


def top_words(words, reverse):
    top = []
    if reverse:
        top = words[:10]
    else:
        top = words[-1:-11:-1]
    return top


def frequency_thresholds(words):
    """!!!!!! доделать"""
    print('Исключение редко встречающихся слов (например, с частотой < N).')
    print('Для исключения слов из списка с частотой N и меньше, введите N')
    print('Если исключать слова из списка не нужно, введите 0')
    number_n = int(input('Введите N: '))
    if number_n > 0:
        new_words = [pair for pair in words if pair[1] > number_n]
    else:
        new_words = words[:]
    return new_words



words_dict = main_menu()

reverse_flag = selection_sorting()

# Если reverse_flag == True, то (-1)^1, т.е. сортировка производится по убыванию, иначе - по возрастанию
sorted_words = sorted(words_dict.items(), key=lambda w: ((-1) ** reverse_flag * w[1], w[0]))
print(sorted_words)

if len(words_dict) <= 500:
    print_result(sorted_words)
else:
    print('Количество слов превышает 500. Результат можете посмотреть в файле "result.txt".')

with open('result.txt', 'w', encoding='utf-8') as file:
    print_result(sorted_words, file)


print('Общее количество слов:', sum(words_dict.values()))

print('Топ-10 слов:')
print_result(top_words(sorted_words, reverse_flag))

new_words = frequency_thresholds(sorted_words)
print_result(new_words)

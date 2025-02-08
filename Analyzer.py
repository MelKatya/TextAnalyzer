import re
from typing import Dict, List, Generator
from concurrent.futures import ProcessPoolExecutor
from functools import partial
import os
from math import ceil


def words_count(lines: List[str], stop_words: List[str]) -> Dict[str, int]:
    """
    Заполняет словарь частоты слов в списке строк текста.

    Args:
        lines (List[str]): список строк текста.
        stop_words (List[str]): список стоп-слов, которые не учитываются в подсчете.

    Returns:
        Dict[str, int]: словарь частоты слов (слово: частота).
    """

    result = {}
    chunk_size = ceil(len(lines) / 10)
    template = re.compile(r"[a-zA-Zа-яА-Я]+[-]?[']?[a-zA-Zа-яА-Я]*")  # шаблон для поиска слов

    for start in range(0, len(lines), chunk_size):
        chunk = lines[start:start + chunk_size]
        # Объединяем строки, чтобы разом обрабатывать большее количество слов
        chunk_text = ' '.join(chunk).lower()
        words_line = template.findall(chunk_text)

        for word in words_line:
            if word not in stop_words:
                result[word] = result.get(word, 0) + 1

    return result


def print_result(sorted_list: List, file=None) -> None:
    """
    Выводит в консоль или в файл результатов.

    Args:
        sorted_list (List): отсортированный список кортежей (слово, частота).
        file : если None, вывод происходит в консоль, иначе - в файл.
    """

    # ищем самое длинное слово
    len_word = max(map(lambda word: len(word[0]), sorted_list)) + 2

    print(f'{"_" * (len_word + 12)}', file=file)
    print(f'|{"Слово":^{len_word}}| Частота |', file=file)
    print(f'|{"-" * len_word}|{"-" * 9}|', file=file)
    for word in sorted_list:
        print(f'|{word[0]:^{len_word}}|{word[1]:^9}|', file=file)
    print(f'{"¯" * (len_word + 12)}', file=file)


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

                control_check = re.findall(r"[a-zA-Zа-яА-Я]+[-]?[']?[a-zA-Zа-яА-Я]*", stop_words)
                stop_words = stop_words.split()

                # сравниваем списки, чтобы убедиться, что пользователь не ввел посторонние символы
                if control_check == stop_words:
                    return stop_words
                else:
                    print('Ошибка ввода. В словах могут присутствовать только буквы и дефис("-").')

        else:
            print('Неверно сделан выбор. Введите 1 или 0.')


def read_lines_chunks(file_path: str, chunk_size: int) -> Generator:
    """
    Генерирует чанки строк из текстового файла.


    Args:
        file_path (str): путь к текстовому файлу.
        chunk_size (int): размер чанка (количество строк).

    Returns:
        Generator : чанк строк.
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        chunk = []
        for line in file:
            chunk.append(line.strip())
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk


def merge_results(results: List) -> Dict[str, int]:
    """
    Объединяет частотные словари в один.

    Args:
        results (List): список частотных словарей.

    Returns:
        Dict[str, int]: объединенные частотные словари.
    """

    final_result = {}
    for result in results:  # Перебираем частотные словари
        for word, count in result.items():  # Обновляем итоговый словарь
            final_result[word] = final_result.get(word, 0) + count

    return final_result


def process_chunk(chunk: list[str], stop_words: list[str]) -> Dict[str, int]:
    """
     Передает stop_words в функцию words_count.

    Args:
        chunk (list[str]): один чанк (список строк).
        stop_words (list[str]): список стоп-слов.

    Returns:
        Dict[str, int]: частотный словарь одного чанка.
    """
    return words_count(chunk, stop_words)


def calculate_avg_line_size(file_path: str, num_samples: int = 100) -> int:
    """
    Рассчитывает среднюю длину строк в файле на основе выборки.

    Args:
        file_path (str): путь к файлу.
        num_samples (int): количество строк для выборки.

    Returns:
        int: средняя длина строк в символах.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        sample_lines = [len(f.readline()) for _ in range(num_samples)]
    return sum(sample_lines) // len(sample_lines)


def parallel_processing(file_size: int, file_path: str, stop_words: List[str]) -> Dict[str, int]:
    """
    Разбивает файл на чанки и параллельно их обрабатывает.

    Args:
        file_size (int): размер файла.
        file_path (str): путь к файлу.
        stop_words (List[str]): список стоп-слов.

    Returns:
        Dict[str, int]: словарь частоты слов из файла.
    """
    avg_line_size = calculate_avg_line_size(file_path)

    chunk_size = ceil(file_size / (40 * avg_line_size))
    chunks = read_lines_chunks(file_path, chunk_size=chunk_size)
    print('herre')
    # Для передачи стоп-слов в функцию подсчета слов
    process_with_stopwords = partial(process_chunk, stop_words=stop_words)

    with ProcessPoolExecutor(max_workers=None) as executor:
        # Параллельно обрабатываем чанки
        results = list(executor.map(process_with_stopwords, chunks))

    # Объединяем результаты
    return merge_results(results)



def load_file(stop_words: List[str]) -> Dict[str, int]:
    """
    Загружает текст из файла и подсчитывает частоту слов.

    Args:
        stop_words (List[str]): список стоп-слов.

    Returns:
        Dict[str, int]: словарь частоты слов из файла.
    """

    file_path = input('\nУкажите полный путь до файла в формате .txt: ')
    while not (os.path.isfile(os.path.abspath(file_path)) and file_path.endswith('.txt')):
        file_path = r'C:\TextAnalyzer\my_text.txt'
        print('Неверно указан путь до файла или нет к нему доступа. Повторите ввод!')
        #file_path = input('\nУкажите полный путь до файла .txt: ')

    file_size = os.path.getsize(file_path)
    file_size_threshold = 5 * 1024 * 1024  # 5 MB

    # Если файл больше 5MB, то он разбивается на чанки и обрабатывает их параллельно
    if file_size > file_size_threshold:
        result = parallel_processing(file_size, file_path, stop_words)

    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            all_text = f.readlines()
        result = words_count(all_text, stop_words)

    return result


def write_text(stop_words: List[str]) -> Dict[str, int]:
    """
    Принимает текстовый ввод от пользователя для анализа частоты слов.

    Args:
        stop_words (List[str]): список стоп-слов.

    Returns:
        Dict[str, int]: словарь из слов частоты слов из текста.
    """

    print('\nВведите текст для анализа:\n'
          '(для прекращения ввода напишите на пустой строке _1 и нажмите enter):')
    original_text = "\n".join(iter(input, "_1"))

    while not original_text:
        print('Текст не может быть пустым. Повторите ввод!')
        original_text = "\n".join(iter(input, "_1"))

    words = words_count(original_text.split('\n'), stop_words)
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
              '\t1 - Показать на экране;\n'
              '\t2 - Не выводить.')
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


if __name__ == "__main__":
    words_dict = main_menu()

    filtered_words = frequency_thresholds(words_dict)
    reverse_flag = selection_sorting()
    # Если reverse_flag == True, то (-1)^1 == -1, т.е. сортировка производится по убыванию,
    # иначе (-1)^0 == 1 - сортировка по возрастанию
    sorted_words = sorted(filtered_words, key=lambda w: ((-1) ** reverse_flag * w[1], w[0]))

    if len(filtered_words) <= 500:
        print_result(sorted_words)
        print('Общее количество слов:', sum(words_dict.values()))
    else:
        print('Количество слов превышает 500. Результат можете посмотреть в файле "result.txt".')

    with open('result.txt', 'w', encoding='utf-8') as file:
        print_result(sorted_words, file=file)
        print(f'Общее количество слов: {sum(words_dict.values())}', file=file)

    top_words(sorted_words, reverse_flag)

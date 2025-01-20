import re
from typing import Dict


def words_count(text: str, result) -> Dict:
    template = re.compile(r'[^\d,\W]+[-]?\w*')
    words = template.findall(text.lower())
    for word in words:
        if result.get(word):
            result[word] += 1
        else:
            result[word] = 1
    return result


def print_result(result_dict, file=None):
    print(f'{"_" * 37}', file=file)
    print(f'|{"Слово":^25}| Частота |', file=file)
    print(f'|{"-" * 25}|{"-" * 9}|', file=file)
    for word, frequency in dict(result_dict).items():
        print(f'|{word:^25}|{frequency:^9}|', file=file)
    print(f'{"¯" * 37}', file=file)


words_dict = None
print('Укажите источник текста:\n'
      '1 - Текстовый файл;\n'
      '2 - Ввод текста в консоль.')
text_source = input('Ввод: ')

words_dict = dict()
if text_source == '1':
    my_file = r'C:\TextAnalyzer\allpart.txt'
    file_path = input('Укажите полный путь до файла: ')

    try:
        with open(my_file, 'r', encoding='utf-8') as file:

            for line in file:
                words_dict = words_count(line, words_dict)

    except FileNotFoundError:
        print('Неверно указан путь до файла.')
    except FileExistsError:
        print('Нет доступа к файлу.')

elif text_source == '2':
    original_text = input('Введите текст для анализа:\n')
    words_dict = words_count(original_text, words_dict)

else:
    print('Неверно указан источник текста. Введите 1 или 2.')

print('Выберете сортировку слов по частоте:\n'
      '1 - По убыванию;\n'
      '2 - По возрастанию.')
sorted_choice = input('Ввод: ')

reverse_flag = True
if sorted_choice == '1':
    reverse_flag = True
elif sorted_choice == '2':
    reverse_flag = False
else:
    print('Неверно выбрана сортировка. Введите 1 или 2.')

sorted_words = sorted(words_dict.items(), key=lambda w: w[1], reverse=reverse_flag)

if len(words_dict) <= 500:
    print_result(sorted_words)
else:
    print('Количество слов превышает 500. Результат будет записан в файл "result.txt".')

with open('result.txt', 'w', encoding='utf-8') as file:
    print_result(sorted_words, file)


print('Общее количество слов:', sum(words_dict.values()))
# print('Топ-10 слов:')
# print(dict(sorted_words[:10]))
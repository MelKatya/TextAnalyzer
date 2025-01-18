import re
from typing import Dict


def words_count(text: str) -> Dict:
    result = {}
    template = re.compile(r'[^\d,\W]+[-]?\w*')
    words = template.findall(text.lower())
    for word in words:
        if result.get(word):
            result[word] += 1
        else:
            result[word] = 1
    return result


words_dict = None
print('Укажите источник текста:\n'
      '1 - Текстовый файл;\n'
      '2 - Ввод текста в консоль.')
text_source = input('Ввод: ')

if text_source == '1':
    my_file = 'C:\TextAnalyzer\my_text.txt'
    file_path = input('Укажите полный путь до файла: ')

    try:
        with open(my_file, 'r', encoding='utf-8') as file:
            words_dict = words_count(file.read())
    except FileNotFoundError:
        print('Неверно указан путь до файла.')
    except FileExistsError:
        print('Нет доступа к файлу.')

elif text_source == '2':
    original_text = input('Введите текст для анализа:\n')
    words_dict = words_count(original_text)

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

for word, frequency in dict(sorted_words).items():
    print(f'{word}: {frequency}')

print('Общее количество слов:', len(words_dict))
# print('Топ-10 слов:')
# print(dict(sorted_words[:10]))
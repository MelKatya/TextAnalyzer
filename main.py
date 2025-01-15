import re

template = re.compile(r'[^\d,\W]+[-]?\w*')
words_dict = {}
with open('my_text.txt', 'r', encoding='utf-8') as file:
    for line in file:
        words = template.findall(line.lower())
        for word in words:
            if words_dict.get(word):
                words_dict[word] += 1
            else:
                words_dict[word] = 1


for word, frequency in words_dict.items():
    print(f'{word}: {frequency}')
print(len(words_dict))

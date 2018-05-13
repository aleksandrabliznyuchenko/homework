from random import choice

from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()

from flask import Flask
from flask import request, render_template


app = Flask(__name__)


## Создаём словарь из скачанных словоформ (который получается большим по объему, из-за чего сам сайт на Flask долго грузится)
## На подборках словоформ меньшего размера работает хорошо
## Тестировалось на файле 'wordforms_test.txt' (300 случайно выбранных из общего файла словоформ + 100 наиболее частотных)
## Например, "Бойцовский клуб" трансформировалось в "Пилорический заезд"
def dictionary_maker():
    bigdict = {}
    with open('wordforms.txt', 'r', encoding = 'utf-8') as file:
        for line in file:
            form = line.split()[-1]
            form = form.lower()
            ana = morph.parse(form)[0]
            bigdict[form] = {'normal_form': str(ana.normal_form), 'tag': str(ana.tag)}
    return bigdict


## Функция, которая анализирует подаваемое ей слово и подбирает ему рандомный аналог из созданного словаря по тэгу
## Если аналога введённому слову не находится, программа сообщит об этом
def exchange(word, bigdict):
    candidates = []
    ana = morph.parse(word)[0]
    for key in bigdict:
        if str(ana.tag) in bigdict[key]['tag']:
            candidates.append(key)
    if candidates != []:
        random_form = choice(candidates)
    else:
        random_form = '-- Не найдено аналога для слова "' + word + '" --'
    return random_form 


## Делим фразу на слова, пропускаем каждое через замену слова и переписываем исходное предложение
def new_phrase_maker(insert, bigdict):
    words = insert.split()
    sentence = ''
    for i in range(len(words)):
        word = words[i]
        if i == 0:
            sentence = exchange(word, bigdict).capitalize() + ' '
        elif i == len(words) - 1:
            sentence += exchange(word, bigdict)
        else:
            sentence += exchange(word, bigdict) + ' '
    print(sentence)
    return sentence


@app.route('/')            
def index():
    insert = 'Исходная фраза:'
    sentence = 'Это предложение в дальнейшем изменится'
    bigdict = dictionary_maker()
    if request.args:
        insert = request.args['input_phrase']
        sentence = new_phrase_maker(insert, bigdict)
    return render_template('index.html', insert = insert, sentence = sentence)


if __name__ == "__main__":
    app.run(debug=True)

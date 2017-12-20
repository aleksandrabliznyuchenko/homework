from flask import Flask
from flask import request, render_template
import html, os, re, urllib.request


alphabet = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ж': 'j',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'c',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shh',
    'э': 'ee',
    'ю': 'ju',
    'я': 'ja'
    }


app = Flask(__name__)


@app.route('/') # главная страница со сводкой погоды и формой
def index():
    page = urllib.request.urlopen('https://www.gismeteo.ru/weather-skopje-3253/')
    text = page.read().decode('utf-8')
    weather = re.findall('<a class="tab tablink tooltip".*? <div class="tab-icon">', text, re.DOTALL)
    regTag = re.compile('<.*?>', re.DOTALL)
    weather = regTag.sub('', str(weather))
    weather = weather.replace('[', '')
    weather = weather.replace(']', '')
    weather = weather.replace('\\n', '')
    weather = weather.replace('\'', '')
    weather = html.unescape(weather)
    return render_template('form.html', weather=weather)


@app.route('/old_Russianed') # транслитерация введённого слова в соответствии со словарём дореволюционных написаний
def old_Russianed():
    old_Russian = {}
    rus_word = request.args['input_word']
    lowered_word = rus_word.lower()
    letter = alphabet[lowered_word[0]]
    with open(os.path.join(r'C:\Users\AleksandraB\Desktop\Programmin~\alphabet', letter + '.tsv'), 'r', encoding = 'utf-8') as f:
        for line in f:
            words = line.split('\t')
            old_Russian[words[1]] = words[3]
        if rus_word in old_Russian:
            word = old_Russian[rus_word]
            return render_template('old_Russianed.html', word=word)
        else:
            if lowered_word in old_Russian:
                word = old_Russian[lowered_word]
                return render_template('old_Russianed.html', word=word)
            else:
                return 'Такого слова не найдено в словаре правильных дореволюционных написаний'

            
@app.route('/daily_news') # забираем тексты с новостного ресурса, пропускаем слова через mystem и сравниваем лексемы со словарём
def daily_news():
    page = urllib.request.urlopen('https://yle.fi/uutiset/osasto/novosti/')
    text = page.read().decode('utf-8')
    regTag = re.compile('<.*?>', re.DOTALL)
    regLine = re.compile('\\n', re.DOTALL)
    news = re.findall('<h1>.*?</h1>', text, re.DOTALL)
    news = html.unescape(news)
    clear_news = regTag.sub('', str(news))
    clear_news = regLine.sub('', clear_news)
    clear_news = clear_news.replace('\\n', '')
    article = re.findall('<p>.*?<span class="meta">', text, re.DOTALL)
    article = html.unescape(article)
    clear_article = regTag.sub('', str(article))
    clear_article = regLine.sub('', clear_article)
    clear_article = clear_article.replace('\\n', '')

    with open('input_news.txt', 'w', encoding = 'utf-8') as f1:
        f1.write(clear_news)
        f1.write(clear_article)
        
    os.system(r"C:\Users\AleksandraB\Desktop\Programmin~\mystem.exe input_news.txt output_news.txt")
    with open('output_news.txt', 'r', encoding = 'utf-8') as f2:
        text = f2.read()
        lexemes = re.findall('{.*?}', text, re.DOTALL)
        for lexeme in lexemes:
            old_Russian_dict = {}
            lexemes_dict = {}
            lexeme = lexeme.replace('{', '')
            lexeme = lexeme.replace('}', '')
            lowered_lexeme = lexeme.lower()
            try:
                letter = alphabet[lowered_lexeme[0]]
                with open(os.path.join(r'C:\Users\AleksandraB\Desktop\Programmin~\alphabet', letter + '.tsv'), 'r', encoding = 'utf-8') as f:
                    for line in f:
                        words = line.split('\t')
                        old_Russian_dict[words[1]] = words[3]
                    if lexeme in old_Russian_dict:
                        word = old_Russian_dict[lexeme]
                        with open('translitered.txt', 'a', encoding = 'utf-8') as f3:
                            f3.write(word + '; ')
                    else:
                        if lowered_lexeme in old_Russian_dict:
                            word = old_Russian_dict[lowered_lexeme]
                            with open('translitered.txt', 'a', encoding = 'utf-8') as f3:
                                f3.write(word + '; ')
                        else:
                            continue
            except KeyError:
                continue

    with open('translitered.txt', 'r', encoding = 'utf-8') as f4:
            transliteration = f4.read()
            return render_template('news.html', transliteration=transliteration)
            
            
@app.route('/test') # страница с тестом
def test():
    return render_template('test.html')


@app.route('/results') # результаты теста
def results():
    result = 0
    if request.args['music'] == 'music_E':
        result +=1
    if request.args['old'] == 'old_e':
        result += 1
    if request.args['April'] == 'April_E':
        result += 1
    if request.args['sparrow'] == 'sparrow_e':
        result += 1
    if request.args['family'] == 'family_e':
        result += 1
    if request.args['twelve'] == 'twelve_E':
        result += 1
    if request.args['girl'] == 'girl_E':
        result += 1
    if request.args['bed'] == 'bed_e':
        result += 1
    if request.args['lion'] == 'lion_e':
        result += 1
    if request.args['star'] == 'star_E':
        result += 1
    return render_template('results.html', result=result)

    
if __name__ == '__main__':
    app.run(debug=True)

        

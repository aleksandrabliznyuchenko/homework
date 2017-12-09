from flask import Flask
from flask import request, render_template, url_for
import json


app = Flask(__name__)


@app.route('/')
def index():
    urls = {'Главная  страница': url_for('index'),
            'Результаты в систематизированном виде': url_for('stats'),
            'Json со всеми введенными на сайте данными': url_for('jsoned'),
            'Поиск': url_for('search'),
            'Результаты поиска': url_for('results')
            }
    return render_template('index.html')


@app.route('/stats')
def stats():
    cities = []
    answers = 0
    male = 0
    female = 0
    age_sum = 0
    if request.values['sex'] == 'male':
        male += 1
    elif request.values['sex'] == 'female':
        female += 1
    answers = male + female
    if request.values['living_city'] not in cities:
        city = cities.append(request.values['living_city'])
    percent_male = (male/answers)*100
    percent_female = (female/answers)*100
    with open('data.json', 'a', encoding = 'utf-8') as f1:
        json.dump(request.args, f1, ensure_ascii = False)
    return render_template('stats.html', answers=answers, percent_male=percent_male,
                           percent_female=percent_female, cities=cities)


@app.route('/json')
def jsoned():
    with open('data.json', 'r', encoding = 'utf-8') as f2:
        data_from_json = f2.read()
    return data_from_json


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/results')
def results():
    return render_template('results.html') # это очень плохо, но результатов поиска у меня нет


if __name__ == '__main__':
    app.run(debug=True)

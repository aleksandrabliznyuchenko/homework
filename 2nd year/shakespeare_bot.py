from collections import defaultdict
from random import uniform
import flask
import re
import telebot
import os

# марковская модель
def gen_lines(corpus):
    with open(corpus, 'r', encoding = 'utf-8') as data:
        lines = data.readlines()
        return lines


def gen_tokens(lines):
    symbols = re.compile(r'[а-яА-Я0-9-]+|[.,:;?!]+')
    for line in lines:
        for token in symbols.findall(line):
            yield token


def gen_trigrams(tokens):
    t0, t1 = '$', '$'
    for t2 in tokens:
        yield t0, t1, t2
        if t2 in '.!?':
            yield t1, t2, '$'
            yield t2, '$','$'
            t0, t1 = '$', '$'
        else:
            t0, t1 = t1, t2


def train(corpus):
    lines = gen_lines(corpus)
    tokens = gen_tokens(lines)
    trigrams = gen_trigrams(tokens)

    bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for t0, t1, t2 in trigrams:
        bi[t0, t1] += 1
        tri[t0, t1, t2] += 1

    model = {}
    for (t0, t1, t2), freq in tri.items():
        if (t0, t1) in model:
            model[t0, t1].append((t2, freq/bi[t0, t1]))
        else:
            model[t0, t1] = [(t2, freq/bi[t0, t1])]
    return model


def generate_sentence(model):
    phrase = ''
    t0, t1 = '$', '$'
    while 1:
        t0, t1 = t1, unirand(model[t0, t1])
        if t1 == '$': break
        if t1 in ('.!?,;:') or t0 == '$':
            phrase += t1
        else:
            phrase += ' ' + t1
    return phrase.capitalize()


def unirand(seq):
    sum_, freq_ = 0, 0
    for item, freq in seq:
        sum_ += freq
    rnd = uniform(0, sum_)
    for token, freq in seq:
        freq_ += freq
        if rnd < freq_:
            return token

#тренировка модели
model = train('shakespeare.txt')

# начало игр с Хероку
TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(TOKEN, threaded = False)

bot.remove_webhook()
bot.set_webhook(url= 'https://talk-like-shakespeare.herokuapp.com/bot')

app = flask.Flask(__name__)

# риветственное сообщение бота
@bot.message_handler(commands = ['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hey there! Write me something new and I will respond in a Shakespearen way.')

# выдача строки в шекспировском стиле после того, как нам что-то напишут
@bot.message_handler(func = lambda m: True)
def send_shakespeare(message):
    shakespeare = generate_sentence(model)
    bot.send_message(message.chat.id, shakespeare)

# главная страница проверки, что в целом все загружено
@app.route("/", methods=['GET', 'HEAD'])
def index():
    return 'ok'

# страница бота
@app.route('/bot', methods = ['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port)

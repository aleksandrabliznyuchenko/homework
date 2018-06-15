from collections import defaultdict
from random import uniform
import flask
import re
import telebot
import conf


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


def generate_sentence(model, word):
    t0 = '$'
    if word != '':
        phrase = word.capitalize()
        t1 = phrase
    else:
        phrase = ''
        t1 = '$'
    while 1:
        t0, t1 = t1, unirand(model[t0, t1])
        if t1 == '$':
            break
        if t1 in ('.!?,;:') or t0 == '$':
            phrase += t1
        else:
            phrase += ' ' + t1
    return phrase


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
model = train(shakespeare.txt)
# или model = train('/home/Ilma/shakespearean/shakespeare.txt') для кода, лежащего на pythonanywhere



# начало настройки бота
WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded = False)

bot.remove_webhook()
bot.set_webhook(url = WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

# приветственное сообщение бота
@bot.message_handler(commands = ['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hey there! Write me something new and I will respond in a Shakespearean way.')

# выдача строки в шекспировском стиле после того, как нам что-то напишут
@bot.message_handler(func = lambda m: True)
def send_shakespeare(message):
    words = message.text.split()
    try:
        shakespeare = generate_sentence(model, words[-1].strip('.,!?:;'))
        bot.send_message(message.chat.id, shakespeare)
    except KeyError:
        shakespeare = generate_sentence(model, '')
        bot.send_message(message.chat.id, shakespeare)

# главная страница проверки, что в целом все загружено
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

# функция, запускающаяся, когда к нам обращается Telegram
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


if __name__ == '__main__':
    bot.polling(none_stop=True)

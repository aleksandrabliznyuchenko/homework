from flask import Flask
from flask import request

app = Flask(__name__)

codes = {}

with open ('lang.tsv', 'r', encoding = 'utf-8') as f:
    for lines in f:
        elems = lines.split('\t')
        codes[elems[0]] = elems[1:4]


@app.route('/language')
def language():
    if request.args['lang'] != None:
        lang = request.args['lang']
        if lang in codes:
            language = codes[request.args['lang']]
            code = ', '.join(language)
            return 'ISO-код языка: ' + code
        else:
            key = lang.capitalize()
            language = codes[key]
            code = ', '.join(language)
            return 'ISO-код языка: ' + code
    else:
        print('None')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route('/')
def thanks():
    return 'Спасибо за помощь!'

@app.route('/form')
def form():
    with open('data.txt', 'a', encoding = 'utf-8') as f1: # надо бы в json
        json.dump(request.args, f1, ensure_ascii = False)

def data_design():
    # надо преобразовать странные ключи-значения словаря в русский вариант

@app.route('/stats')
def stats():
    with open('data.txt', 'r', encoding = 'utf-8') as f2:
        for line in f2:
            return line
            

##@app.route('/json')
##def json_load():
##    with open('data.txt', 'r', encoding = 'utf-8') as f3:
##        json_data = json.load(f3)
##        return json_data


##@app.route('/json')
##def index():
##    if request.args['sex'] in request.args:
##        file = open('data.json', 'w', encoding = 'utf-8')
##        data = json.dump(request.args, file)
##        file.close()
##        return(file)

##@app.route('/json')
##def json():
##    file = open('data.json', 'r', encoding = 'utf-8')
##    text = json.load(request.args, file)
##    #print(text)
##    file.close()
##    return(text)

if __name__ == '__main__':
    app.run(debug=True)

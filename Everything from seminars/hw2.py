from flask import Flask
from flask import request
from flask import render_template
#import json

app = Flask(__name__)

@app.route('/')
def thanks():
    return '<html><body><p>Спасибо за помощь!</p></body></html>'

##@app.route('/form')
##def form(name=None):
##    return render_template('form.html', age ='age', city='city', education='education')

@app.route('/form')
def form():
    if request.args['age'] == '19':
        return 'It works!'

if __name__ == '__main__'
    app.run(debug=True)

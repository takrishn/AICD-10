from flask import Flask
from flask import render_template

app = Flask(__name__)

#Expectation: List of ICD codes with associated words



@app.route('/')
def hello_world():
    return render_template('main.html')

@app.route('/confirm')
def confirm():
    return render_template('confirm.html', results = [
        ('250.0', "Diabetes mellitus without mention of complication or manifestation classifiable to 250.1-250.9")
        for i in range(0, 5)
    ])


if __name__ == '__main__':
    app.run()

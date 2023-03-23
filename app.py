from flask import Flask, render_template, request
from calculatro import WolframEvaluator
app = Flask(__name__)

params = {
    'result': '',
    'equation': ''
}

wolframSession = WolframEvaluator()

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    global params, wolframSession
    if request.method == 'POST':
        if request.form.get('solveButton') == 'solve':
            params['equation'] = request.form.get('equation')
            params['result'] = wolframSession.solveEquation(params['equation'], stringFormat=True)
    elif request.method == 'GET':
        pass
    return render_template('main.html', **params)

if __name__ == '__main__':
    app.run()

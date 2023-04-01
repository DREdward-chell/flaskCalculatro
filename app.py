from flask import Flask, render_template, redirect, request, url_for
from skeletons import WolframEvaluator

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
            params['result'] = wolframSession.solveEquation(request.form.get('equation'), stringFormat=True)
    elif request.method == 'GET':
        params['result'] = ''
        params['equation'] = ''
    return render_template('main.html', **params)

@app.route('/fff', methods=['GET', 'POST'])
def page2():
    return render_template('geometryDescription.html')

if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, redirect, request, url_for
from skeletons import WolframEvaluator, UserManager

app = Flask(__name__)

params: dict[str, str] = {
    'equation': '',
    'equation_result': ''
}

evaluator: WolframEvaluator = WolframEvaluator()

# entering a website
@app.route('/')
def enter():
    return redirect('/calculatro/main')

# main-page
@app.route('/calculatro/main', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('main.html')

    # redirect to different pages
    elif request.method == 'POST':
        if request.form['equation'] == 'EQUATIONS':
            return redirect('/calculatro/solve-equation')

        elif request.method['graphics'] == 'GRAPHICS':
            return redirect('/calculatro/graphics')

        elif request.method['chemistry'] == 'CHEMISTRY':
            return redirect('/calculatro/molecule-plotting')

        elif request.method['physics'] == 'PHYSICS':
            return redirect('/calculatro/physical-calculations')

        elif request.method['text_from_picture'] == 'TEXT FROM PICTURE':
            return redirect('/calculatro/text-from-picture')

# equation solver
@app.route('/calculatro/solve-equation', methods=['GET', 'POST'])
def solve():
    global evaluator, params

    if request.method == 'GET':
        ...

    elif request.method == 'POST':

        if request.form['solve'] == 'SOLVE':
            params['equation'] = request.form['equation'].strip().replace('\n', '')
            params['equation_result'] = evaluator.solveEquation(params['equation'], stringFormat=True)

    return render_template('equation.html', **params)

@app.route('/calculatro/plot-function', methods=['GET', 'POST'])
def plot():
    pass

@app.route('/calculatro/text-from-picture', methods=['GET', 'POST'])
def get_text():
    pass

@app.route('/caclulatro/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()

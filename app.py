from werkzeug.exceptions import BadRequestKeyError
from flask import Flask, Blueprint, render_template, redirect, request, url_for, jsonify
from skeletons import WolframEvaluator, UserManager


evaluator: WolframEvaluator = WolframEvaluator()


app: Flask = Flask(__name__)


params: dict[str, str] = {
    'scobe': '',
    'calculation_result': '',
    'equation': '',
    'equation_result': '',

    'function': '',
    'xstart': '',
    'xend': '',
    'graph': False,
    'pfunction1': '',
    'pfunction2': '',
    'ustart': '',
    'uend': '',
    'pgraph': False
}


def clear_params():
    global params

    for i in params.keys():
        params[i] = ''


"""-------------------------------------------------------API------------------------------------------------------"""


api = Blueprint('API', __name__)


# error handler
@api.errorhandler(404)
@api.errorhandler(405)
def _api_error(_error):
    if request.path.startswith('/calculatro/api/'):
        return jsonify({'code': _error.code, 'error': str(_error)})
    else:
        return _error


# equation solver
@api.route('/calculatro/api/solve/<equation>')
def solve_equation(equation):
    global evaluator

    try:
        return jsonify(evaluator.solveEquation(equation, stringFormat=True))
    except Exception as error:
        return jsonify(error)


# function plotter
@api.route('/calculatro/api/plot/<function>&<start>&<end>')
def plot_function(function, start, end):
    global evaluator

    try:
        return jsonify(evaluator.plot2d(func=function, xrange=(start, end)))
    except Exception as error:
        return jsonify(error)


"""------------------------------------------------WEB-APPLICATION------------------------------------------------"""


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
        try:
            if request.form['equation'] == 'EQUATIONS':
                return redirect('/calculatro/solve-equation')
        except BadRequestKeyError:
            ...
        try:
            if request.form['graphics'] == 'GRAPHICS':
                return redirect('/calculatro/plot-function')
        except BadRequestKeyError:
            ...
        try:
            if request.form['chemistry'] == 'CHEMISTRY':
                return redirect('/calculatro/molecule-plotting')
        except BadRequestKeyError:
            ...
        try:
            if request.form['physics'] == 'PHYSICS':
                return redirect('/calculatro/physical-calculations')
        except BadRequestKeyError:
            ...
        try:
            if request.form['text'] == 'TEXT':
                return redirect('/calculatro/text-from-picture')
        except BadRequestKeyError:
            ...

    return render_template('main.html')


# equation solver
@app.route('/calculatro/solve-equation', methods=['GET', 'POST'])
def solve():
    global evaluator, params

    if request.method == 'GET':
        return render_template('equation.html', **params)

    elif request.method == 'POST':
        try:
            if request.form['back'] == 'BACK TO MAIN PAGE':
                clear_params()
                return redirect('/calculatro/main')
        except BadRequestKeyError:
            ...
        try:
            if request.form['calculate'] == 'CALCULATE':
                params['scobe'] = request.form['calc'].strip().replace('\n', '').replace('=', '==')
                params['calculation_result'] = evaluator.evaluate(f"ToString[{params['scobe']}]")
                return render_template('equation.html', **params)
        except BadRequestKeyError:
            ...
        try:
            if request.form['solve'] == 'SOLVE':
                params['equation'] = request.form['expression'].strip().replace('\n', '').replace('=', '==')
                params['equation_result'] = evaluator.\
                    solveEquation(params['equation'], stringFormat=True).replace('{', '[').replace('}', ']')
                return render_template('equation.html', **params)
        except BadRequestKeyError:
            ...

    return render_template('equation.html', **params)


@app.route('/calculatro/plot-function', methods=['GET', 'POST'])
def plot():
    global evaluator, params

    if request.method == 'GET':
        return render_template('graphics.html', **params)

    elif request.method == 'POST':
        try:
            if request.form['back'] == 'BACK TO MAIN PAGE':
                clear_params()
                return redirect('/calculatro/main')
        except BadRequestKeyError:
            ...
        try:
            if request.form['plot'] == 'PLOT':
                params['function'] = request.form['expression'].strip().replace('\n', '')
                params['xstart'], params['xend'] = request.form['start'], request.form['end']
                try:
                    evaluator.plot2d(func=params['function'], xrange=(params['xstart'], params['xend']),
                                     path='./static/images/graphic.png')
                except Exception:
                    ...
                params['graph'] = True
        except BadRequestKeyError:
            ...
        try:
            if request.form['pplot'] == 'PLOT':
                params['pfunction1'] = request.form['expression1'].strip().replace('\n', '')
                params['pfunction2'] = request.form['expression2'].strip().replace('\n', '')
                params['ustart'], params['uend'] = request.form['pstart'], request.form['pend']
                try:
                    evaluator.parametricPlot(func1=params['pfunction1'], func2=params['pfunction2'],
                                             urange=(params['ustart'], params['uend']),
                                             path='./static/images/parametric_graphic.png')
                except Exception:
                    ...
                params['pgraph'] = True
        except BadRequestKeyError:
            ...

    return render_template('graphics.html', **params)


@app.route('/calculatro/text-from-picture', methods=['GET', 'POST'])
def get_text():
    pass


@app.route('/calculatro/login')
def login():
    return render_template('login.html')


@app.route('/calculatro/help')
def login():
    return render_template('help.html')


"""------------------------------------------------------START-----------------------------------------------------"""


if __name__ == '__main__':
    app.run()

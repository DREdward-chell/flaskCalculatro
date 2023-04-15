from werkzeug.exceptions import BadRequestKeyError
from flask import Flask, Blueprint, render_template, redirect, request, url_for, jsonify
from skeletons import WolframEvaluator, UserManager, UserAlreadyExistsError, UnknownUserError, WrongPassword


evaluator: WolframEvaluator = WolframEvaluator()


usersDB = UserManager(datasource='./database/database.sqlite')


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
    'pgraph': False,

    'reaction': '',
    'balanced': '',
    'molecule': '',
    'molecule_plot': False,

    'text': '',
    'question': '',
    'answer': '',

    'email': '',
    'username': '',
    'password': '',
    'eu': ''
}


def clear_params():
    global params

    for i in params.keys():
        params[i] = ''


"""-------------------------------------------------------API------------------------------------------------------"""


# api = Blueprint('API', __name__)
#
#
# # error handler
# @api.errorhandler(404)
# @api.errorhandler(405)
# def _api_error(_error):
#     if request.path.startswith('/calculatro/api/'):
#         return jsonify({'code': _error.code, 'error': str(_error)})
#     else:
#         return _error
#
#
# # equation solver
# @api.route('/calculatro/api/solve/<equation>')
# def solve_equation(equation):
#     global evaluator
#
#     try:
#         return jsonify(evaluator.solveEquation(equation, stringFormat=True))
#     except Exception as error:
#         return jsonify(error)
#
#
# # function plotter
# @api.route('/calculatro/api/plot/<function>&<start>&<end>')
# def plot_function(function, start, end):
#     global evaluator
#
#     try:
#         return jsonify(evaluator.plot2d(func=function, xrange=(start, end)))
#     except Exception as error:
#         return jsonify(error)


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
        # redirecting to calculatro functions
        try:
            if request.form['maths'] == 'MATHEMATICS':
                return redirect('/calculatro/maths')
        except BadRequestKeyError:
            ...
        try:
            if request.form['graphics'] == 'GRAPHICS':
                return redirect('/calculatro/plot-function')
        except BadRequestKeyError:
            ...
        try:
            if request.form['chemistry'] == 'CHEMISTRY':
                return redirect('/calculatro/chemistry')
        except BadRequestKeyError:
            ...
        try:
            if request.form['physics'] == 'PHYSICS':
                return redirect('/calculatro/physical-calculations')
        except BadRequestKeyError:
            ...
        try:
            if request.form['text'] == 'TEXT':
                return redirect('/calculatro/text')
        except BadRequestKeyError:
            ...

        try:
            if request.form['login'] == 'LOGIN':
                return redirect('/calculatro/login')
        except BadRequestKeyError:
            ...
        try:
            if request.form['register'] == 'REGISTER':
                return redirect('/calculatro/register')
        except BadRequestKeyError:
            ...
        try:
            if request.form['help'] == 'HELP':
                return redirect('/calculatro/help')
        except BadRequestKeyError:
            ...

    return render_template('main.html')


# equation solver
@app.route('/calculatro/maths', methods=['GET', 'POST'])
def solve():
    global evaluator, params

    if request.method == 'GET':
        return render_template('maths.html', **params)

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
                return render_template('maths.html', **params)
        except BadRequestKeyError:
            ...
        try:
            if request.form['solve'] == 'SOLVE':
                params['equation'] = request.form['expression'].strip().replace('\n', '').replace('=', '==')
                try:
                    params['equation_result'] = evaluator.\
                        solveEquation(params['equation'], stringFormat=True).replace('{', '[').replace('}', ']')
                except Exception:
                    params['equation_result'] = 'error'
                return render_template('maths.html', **params)
        except BadRequestKeyError:
            ...

    return render_template('maths.html', **params)


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
                    params['pgraph'] = True
                except Exception:
                    params['pgraph'] = False
        except BadRequestKeyError:
            ...

    return render_template('graphics.html', **params)


@app.route('/calculatro/chemistry', methods=['GET', 'POST'])
def chemistry():
    global evaluator, params

    if request.method == 'GET':
        return render_template('chemistry.html', **params)

    elif request.method == 'POST':
        try:
            if request.form['back'] == 'BACK TO MAIN PAGE':
                clear_params()
                return redirect('/calculatro/main')
        except BadRequestKeyError:
            ...
        try:
            if request.form['balance'] == 'BALANCE':
                params['reaction'] = request.form['reaction'].strip().replace('\n', '')
                try:
                    params['balanced'] = evaluator.reactionBalance(params['reaction']).replace('-->', '->')
                except Exception:
                    params['balanced'] = 'error'
        except BadRequestKeyError:
            ...
        try:
            if request.form['plot'] == 'PLOT':
                params['molecule'] = request.form['molecule']
                try:
                    evaluator.moleculePlot(params['molecule'], './static/images/molecule.png')
                    params['molecule_plot'] = True
                except Exception:
                    params['molecule_plot'] = False
        except BadRequestKeyError:
            ...

    return render_template('chemistry.html', **params)


@app.route('/calculatro/text', methods=['GET', 'POST'])
def text():
    global params, evaluator

    if request.method == 'GET':
        return render_template('text.html', **params)

    elif request.method == 'POST':
        try:
            if request.form['back'] == 'BACK TO MAIN PAGE':
                clear_params()
                return redirect('/calculatro/main')
        except BadRequestKeyError:
            ...
        try:
            if request.form['find'] == 'FIND ANSWER':
                params['text'] = request.form['text']
                params['question'] = request.form['question']
                try:
                    params['answer'] = evaluator.find_textural_answer(text=params['text'], question=params['question'])
                except Exception:
                    params['answer'] = 'error'
        except BadRequestKeyError:
            ...

    return render_template('text.html', **params)


@app.route('/calculatro/login', methods=['GET', 'POST'])
def login():
    global usersDB, params

    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        try:
            if request.form['back'] == 'BACK TO MAIN PAGE':
                clear_params()
                return redirect('/calculatro/main')
        except BadRequestKeyError:
            ...
        try:
            if request.form['login'] == 'LOGIN':
                flag = None
                eu = request.form['user'].strip()
                if '@' not in eu:
                    flag = 'user'
                    params['username'] = eu
                else:
                    flag = 'email'
                    params['email'] = eu
                params['password'] = request.form['password'].strip()
                result = False
                try:
                    if flag == 'email':
                        result = usersDB.checkUserbyEmail(email=params['email'], password=params['password'])
                    elif flag == 'user':
                        result = usersDB.checkUserbyUsername(username=params['username'], password=params['password'])
                except UnknownUserError:
                    return render_template('login.html', **params)
                except WrongPassword:
                    return render_template('login.html', **params)
                if result:
                    clear_params()
                    return redirect('/calculatro/main')
        except BadRequestKeyError:
            ...

@app.route('/calculatro/register', methods=['GET', 'POST'])
def register():
    global usersDB, params

    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        try:
            if request.form['back'] == 'BACK TO MAIN PAGE':
                clear_params()
                return redirect('/calculatro/main')
        except BadRequestKeyError:
            ...
        try:
            if request.form['register'] == 'REGISTER':
                params['email'] = request.form['email'].strip()
                params['username'] = request.form['username'].strip()
                params['password'] = request.form['password'].strip()
                if params['password'] != request.form['confirm'].strip():
                    return render_template('register.html', **params)
                else:
                    try:
                        usersDB.addUser(email=params['email'], username=params['username'], password=params['password'])
                        return redirect('/calculatro/main')
                    except UserAlreadyExistsError:
                        ...
        except BadRequestKeyError:
            ...

    return render_template('register.html', **params)


@app.route('/calculatro/help', methods=['GET', 'POST'])
def tutor():
    if request.method == 'GET':
        return render_template('help.html')

    if request.method == 'POST':
        return redirect('/calculatro/main')


"""------------------------------------------------------START-----------------------------------------------------"""


if __name__ == '__main__':
    app.run()

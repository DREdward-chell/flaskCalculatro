from flask import Flask, render_template, redirect, request, url_for
from skeletons import WolframEvaluator, UserManager

app = Flask(__name__)

params = {
    'result': '',
    'equation': ''
}

@app.route('/')
def enter():
    return redirect('/main')

@app.route('/main')
def main():
    return render_template('home2.html')

@app.route('/main/solve-equation')
def solve():
    return render_template('equation.html', num=5)

@app.route('/main/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()

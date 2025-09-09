from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/nextButton')
def nextPage():
    return render_template("options.html")

@app.route('/quizPage')
def quizPage():
    return render_template("quiz.html")

@app.route('/maintenance')
def maintenancePage():
    return render_template("maintenance.html")
# @app.route('/sudokuPage')
# def sudokuPage():
#     return render_template("maintenance.html")

# @app.route('/crosswordPage')
# def crosswordPage():
#     return render_template("maintenance.html")

# @app.route('/flipflopPage')
# def flipflopPage():
#     return render_template("maintenance.html")

if __name__ == '__main__':
    app.run(debug = True)
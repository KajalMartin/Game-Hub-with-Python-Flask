from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/nextButton', methods = ['POST'])
def nextPage():
    return render_template("options.html")

@app.route('/quizPage', methods = ['POST'])
def quizPage():
    return render_template("quiz.html")

@app.route('/sudokuPage', methods = ['POST'])
def sudokuPage():
    return render_template("maintenance.html")

@app.route('/crosswordPage', methods = ['POST'])
def crosswordPage():
    return render_template("maintenance.html")

@app.route('/flipflopPage', methods = ['POST'])
def flipflopPage():
    return render_template("maintenance.html")

if __name__ == '__main__':
    app.run(debug = True)
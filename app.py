from flask import Flask, render_template, request, redirect, url_for, session
import time
import random

app = Flask(__name__)
app.secret_key = 'topSecret'

# Sample questions for the quiz
questions = [
    {
        "id":1,
        "question":"What is the largest lake in the world?",
        "options":["Caspian Sea", "Baikal", "Lake Superior", "Ontario"],
        "answer": "Baikal"
    },
    {
        "id":2,
        "question":"What is the capital of Japan?",
        "options":["Beijing", "Tokyo", "Seoul", "Bangkok"],
        "answer": "Tokyo"
    },
    {
        "id":3,
        "question":"Which river is the longest in the world?",
        "options":["Nile", "Mississippi", "Amazon", "Yangtze"],
        "answer": "Nile"
    },
    {
        "id":4,
        "question":"What gas is used to extinguish fire?",
        "options":["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"],
        "answer": "Carbon dioxide"
    },
    {
        "id":5,
        "question":"What animal is the national symbol of Australia?",
        "options":["Crocodile", "Emu", "Koala", "Kangaroo"],
        "answer": "Kangaroo"
    },
    {
        "id":5,
        "question":"Which of the following planets is not a gas giant?",
        "options":["Mars", "Jupiter", "Saturn", "Uranus"],
        "answer": "Mars"
    },
    {
        "id":6,
        "question":"Hitler's party is known as:",
        "options":["Labour Party", "Nazi Party", "Ku-Klux-Klan", "Democratic Party"],
        "answer": "Nazi Party"
    },
    {
        "id":7,
        "question":"For which is Galileo famous?",
        "options":["Developed the telescope", "Discovered four satellites of Jupiter", "Found that the swinging motion of the pendulum results in consistent time measurement", "All of the above"],
        "answer": "All of the above"
    },
    {
        "id":8,
        "question":"Ecology deals with",
        "options":["Birds", "Cell formation", "Relation between organisms and their environment", "Tissues"],
        "answer": "Relation between organisms and their environment"
    },
    {
        "id":9,
        "question":"Which is the largest island?",
        "options":["New Guinea", "Andaman Nicobar", "Greenland", "Hawaii"],
        "answer": "Greenland"
    },
    {
        "id":10,
        "question":"Which one is the hottest continent?",
        "options":["Africa", "South Asia", "North America", "Australia"],
        "answer": "Africa"
    }
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/nextButton')
def nextPage():
    return render_template("options.html")

# Quize Page
@app.route('/quizPage/start')
def start_quiz():
    # Initialize the quiz session
    session["quizScore"] = 0
    session['currentQuestion'] = 0
    session["startTime"] = time.time()
    session["questions"] = random.sample(questions, min(5, len(questions))) #random.sample(population, k) - Returns 5 questions from the list
    return redirect(url_for('show_question'))

@app.route('/quizPage/question')
def show_question():
    currentIndex = session.get('currentQuestion', 0)
    question_list = session.get('questions', [])  # Renamed to avoid conflict

    if currentIndex >= len(question_list):
        return redirect(url_for('show_result'))
    
    question = question_list[currentIndex]

    # Check the progress percentage
    progress = int((currentIndex/len(question_list)) * 100)

    # Calculate the time remaining
    timeElapsed = time.time() - session.get('startTime', time.time())
    timeAllowed = 60
    timeRemaining = max(0, timeAllowed - int(timeElapsed))

    return render_template("quiz_question.html",
                           question=question, 
                           progress=progress,
                           timeRemaining=timeRemaining,  # Fixed variable name
                           currentIndex=currentIndex + 1,
                           total_questions=len(question_list))

@app.route('/quizPage/answer', methods=["POST"])
def check_answer():
    currentIndex = session.get("currentQuestion", 0)
    questions = session.get("questions", [])

    if currentIndex >= len(questions):
        return redirect(url_for("show_result"))

    # Get the user's answer from the form
    userAnswer = request.form.get('answer')
    correctAnswer = questions[currentIndex]["answer"]
    isCorrect = userAnswer == correctAnswer

    # correct answer, then update the score
    if isCorrect:
        session['quizScore'] = session.get('quizScore', 0) + 1

    # move to the next question
    session['currentQuestion'] = currentIndex + 1

    # Check if time is up
    timeElapsed = time.time() - session.get('startTime', time.time())
    timeAllowed = 60
    timeUp = timeElapsed >= timeAllowed

    # If there are more questions and time is not up, redirect to the next question
    if session['currentQuestion'] < len(questions) and not timeUp:
        return redirect(url_for('show_question'))
    else:
        return redirect(url_for("show_result"))

@app.route('/quizPage/result')
def show_result():
    score = session.get('quizScore', 0)
    total = len(session.get('questions', []))
    timeTaken = time.time() - session.get('startTime', time.time())

    # Determine result message based on score
    if score >= 4:
        resultMessage = "Excellent! You're a quiz master!"
        resultClass = 'success'
    elif score >=3:
        resultMessage = "Good job! You know your stuff!"
        resultClass = 'success'
    else:
        resultMessage = "Keep practicing and you'll improve!"
        resultClass = "fail"

    # check if the time ran out
    timeAllowed = 60
    timeUp = timeTaken >= timeAllowed

    if timeUp:
        resultMessage = "Time's up! Try to answer faster next time."
        resultClass = 'fail'

    return render_template('quiz_result.html',
                           score = score,
                           total = total,
                           timeTaken = round(timeTaken, 2),
                           resultMessage = resultMessage,
                           resultClass = resultClass,
                           timeUp = timeUp)

# Maintenance Page
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
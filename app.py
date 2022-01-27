from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from markupsafe import re
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.get('/')
def start_survey():
    """Shows start survey form"""
    return render_template("survey_start.html", survey=survey)


@app.post('/begin')
def redirect_to_survey():
    """Redirects POST request to GET survey display"""
    return redirect('/questions/0')


@app.get('/questions/<int:question_id>')
def ask_question(question_id):
    """asks a survey question"""
    current_question = survey.questions[question_id]
    return render_template(
        "question.html",
        question=current_question,
        question_id=question_id
    )


@app.post('/answer')
def save_answer():
    """save question response to responses and if survey done,
    send user a thank you"""
    question_id = int(request.form.get('question-id'))

    responses.append(request.form.get('answer'))

    if question_id < len(survey.questions):
        return redirect(f"questions/{question_id + 1}")
    else:
        return redirect('/complete')


@app.get('/complete')
def thank_user():
    """Render post-survey message"""

    return render_template("completion.html")

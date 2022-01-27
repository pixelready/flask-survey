from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
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
def ask_question():
    """asks a survey question"""

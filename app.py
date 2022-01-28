from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from markupsafe import re
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "never-tell!"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)




@app.get("/")
def start_survey():
    """Shows start survey form"""

    session["responses"] = []
    
    return render_template("survey_start.html", survey=survey)


@app.post("/begin")
def redirect_to_survey():
    """Redirects POST request to first question"""
    
    return redirect("/questions/0")


@app.get("/questions/<int:question_id>")
def ask_question(question_id):
    """asks a survey question and increments question id"""

    current_question = survey.questions[question_id]
    next_question_id = question_id + 1
    return render_template(
        "question.html", question=current_question, question_id=next_question_id
    )


@app.post("/answer")
def save_answer():
    """save question response to responses and if survey done,
    send user a thank you"""

    answer = request.form.get("answer")
    
    question_id = int(request.form.get("question-id"))
    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses
    
    if question_id < len(survey.questions):
        return redirect(f"questions/{question_id}")
    else:
        return redirect("/complete")


@app.get("/complete")
def thank_user():
    """Render post-survey message"""
    responses = session["responses"]
    print(f"responses in complete: {responses}")
    return render_template("completion.html")

import os
import datetime
import random
import sys

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///selfquiz.db")

types = []
q_types = db.execute("SELECT * FROM question_types")

for q_type in q_types:
    types.append(q_type["question_type"])

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        # Save the question

        # Ensure firstname was submitted
        if not request.form.get("question"):
            return apology("must enter a question", 403)

        # Ensure lastname was submitted
        elif not request.form.get("answer"):
            return apology("must enter an answer", 403)

        # Ensure email was submitted
        elif not request.form.get("choice1"):
            return apology("must enter at least first choice", 403)

        # Ensure phone was submitted
        elif not request.form.get("types"):
            return apology("must select a question type", 403)

        # Ensure agree-term box is checked
        elif not request.form.get("completed"):
            return apology("Validation box must be checked", 403)

        try:
            if request.form.get("choice2") == "":
                db.execute("INSERT INTO questions(user_id, question, answer, choice1, type, createdAt) VALUES(:user_id, :question, :answer, :choice1, :qtype, :datetime)",\
                user_id=session["user_id"], question=request.form.get("question"), answer=request.form.get("answer"), choice1=request.form.get("choice1"),\
                qtype=request.form.get("types"), datetime=datetime.date.today())
            elif request.form.get("choice2") != "" and request.form.get("choice3") == "":
                db.execute("INSERT INTO questions(user_id, question, answer, choice1, choice2, type, createdAt) VALUES(:user_id, :question, :answer, :choice1, :choice2, :qtype, :datetime)",\
                user_id=session["user_id"], question=request.form.get("question"), answer=request.form.get("answer"), choice1=request.form.get("choice1"),\
                choice2=request.form.get("choice2"), qtype=request.form.get("types"), datetime=datetime.date.today())
            elif request.form.get("choice2") != "" and request.form.get("choice3") != "":
                db.execute("INSERT INTO questions(user_id, question, answer, choice1, choice2, choice3, type, createdAt) VALUES(:user_id, :question, :answer, :choice1, :choice2, :choice3, :qtype, :datetime)",\
                user_id=session["user_id"], question=request.form.get("question"), answer=request.form.get("answer"), choice1=request.form.get("choice1"),\
                choice2=request.form.get("choice2"), choice3=request.form.get("choice3"), qtype=request.form.get("types"), datetime=datetime.date.today())
            elif request.form.get("choice2") == "" and request.form.get("choice3") != "":
                db.execute("INSERT INTO questions(user_id, question, answer, choice1, choice2, type, createdAt) VALUES(:user_id, :question, :answer, :choice1, :choice2, :qtype, :datetime)",\
                user_id=session["user_id"], question=request.form.get("question"), answer=request.form.get("answer"), choice1=request.form.get("choice1"),\
                choice2=request.form.get("choice3"), qtype=request.form.get("types"), datetime=datetime.date.today())
            else:
                raise Exception()

        except:
            return apology("Memento could not be saved", 403)

        flash("Memento is saved!", 'success')

        return redirect("/")
    else:
        #Create quiz question table if not exist
        db.execute("CREATE TABLE IF NOT EXISTS 'questions' ('id' INTEGER NOT NULL, 'user_id' INTEGER NOT NULL, 'question' TEXT NOT NULL, 'answer' TEXT NOT NULL, 'choice1' TEXT NOT NULL,\
                    'choice2' TEXT NULL DEFAULT NULL, 'choice3' TEXT NULL DEFAULT NULL, `createdAt` DATETIME NOT NULL, `updatedAt` DATETIME NULL DEFAULT NULL,\
                    'type' VARCHAR(50) NOT NULL, 'active' TINYINT(1) NOT NULL DEFAULT 1, PRIMARY KEY ('id'));")

        """Show user's previously created questions"""
        rows = db.execute("SELECT * FROM questions WHERE user_id=:user_id", user_id=session["user_id"])
        questions = []
        answer_choice = []
        choices = []
        questiontype = []

        random.shuffle(rows)
        rows = rows[:min(len(rows),10)]

        for row in rows:
            questions.append(row["question"])
            answer_choice.append(row["answer"])
            answer_choice.append(row["choice1"])
            if row["choice2"]:
                answer_choice.append(row["choice2"])
            if row["choice3"]:
                answer_choice.append(row["choice3"])
            choices.append(answer_choice[:])
            answer_choice.clear()
            questiontype.append(row["type"])

        shuffledChoices = []
        for choice in choices:
            shuffle=choice[:]
            random.shuffle(shuffle)
            shuffledChoices.append(shuffle[:])
            shuffle.clear()

        length = len(questions)

        return render_template("index.html", questions=questions, choices=choices, questiontype=questiontype, length=length, shuffledChoices=shuffledChoices, types=types)


@app.route("/memento", methods=["GET", "POST"])
@login_required
def memento():
    """Share quizes"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        #Create quiz question table if not exist

        db.execute("CREATE TABLE IF NOT EXISTS 'quizes' ('id' INTEGER NOT NULL, 'user_id' INTEGER NOT NULL, 'quiz_name' TEXT NOT NULL, 'questions' TEXT NOT NULL,\
                `createdAt` DATETIME NOT NULL, `updatedAt` DATETIME NULL DEFAULT NULL, 'quiz_type' VARCHAR(50) NOT NULL, 'active' TINYINT(1) NOT NULL DEFAULT 1, PRIMARY KEY ('id'));")

        questions = request.form.get("question-list")
        quiz_name = request.form.get("quiz_name")

        # Ensure agree-term box is checked
        if not request.form.get("quiz_name"):
            quiz_name = "My Quiz"

        quiz_type = ""
        question_list = questions.split(',')

        for question in question_list:
            temp_quiz_type = (db.execute("SELECT type FROM questions WHERE id=:question", question=question))[0]['type']
            if quiz_type != "":
                if quiz_type != temp_quiz_type:
                    quiz_type= "General"
                    break
            else:
                quiz_type = temp_quiz_type


        db.execute("INSERT INTO quizes(user_id, quiz_name, questions, createdAt, quiz_type) VALUES(:user_id, :quiz_name, :questions, :createdAt, :quiz_type)",\
        user_id=session["user_id"], quiz_name=quiz_name, questions=questions, createdAt=datetime.date.today(), quiz_type=quiz_type)

        flash('Quiz is successfully created!', 'success')
        # Redirect user to main page
        return redirect("/memento")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        #Get questions of the current user
        rows = db.execute("SELECT * FROM questions WHERE user_id=:user_id", user_id=session["user_id"])
        questions = []
        answer_choice = []
        choices = []
        questiontype = []
        questID = []

        for row in rows:
            questions.append(row["question"])
            questID.append(row["id"])
            answer_choice.append(row["answer"])
            answer_choice.append(row["choice1"])
            if row["choice2"]:
                answer_choice.append(row["choice2"])
            if row["choice3"]:
                answer_choice.append(row["choice3"])
            choices.append(answer_choice[:])
            answer_choice.clear()
            questiontype.append(row["type"])

        length = len(questions)

        return render_template("memento.html", questions=questions, choices=choices, questiontype=questiontype, length=length, questID=questID)

@app.route("/editmemento", methods=["GET", "POST"])
@login_required
def edit_memento():
    """Edit Question"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        questID = request.form.get("questionID")
        row = (db.execute("SELECT * FROM questions WHERE id=:quest_id", quest_id=questID))[0]
        question=row["question"]
        answer=row["answer"]
        choice1=row["choice1"]
        choice2=row["choice2"]
        choice3=row["choice3"]
        qtype=row["type"]
        quest_id = row["id"]

        if choice2 == None:
            choice2 = ""
        if choice3 == None:
            choice3 = ""

        return render_template("editmemento.html", question=question, answer=answer, qtype=qtype, choice1=choice1, choice2=choice2, choice3=choice3, types=types, quest_id=quest_id)


@app.route("/save_editted_question", methods=["GET", "POST"])
@login_required
def save_editted_memento():
    """Edit Question"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        question=request.form.get("question")
        answer=request.form.get("answer")
        choice1=request.form.get("choice1")
        choice2=request.form.get("choice2")
        choice3=request.form.get("choice3")
        q_type=request.form.get("types")
        quest_id=request.form.get("questionID")

        '''
        print(question, file=sys.stderr)
        print(answer, file=sys.stderr)
        print(choice1, file=sys.stderr)
        print(choice2, file=sys.stderr)
        print(choice3, file=sys.stderr)
        print(q_type, file=sys.stderr)
        print(quest_id, file=sys.stderr)
        '''

        if (not choice2 == "None" and not choice2 == "") and (choice3 == "None" or choice3 == ""):
            db.execute("UPDATE questions SET choice2=:choice2, choice3=NULL WHERE id=:quest_id",\
            choice2=choice2, quest_id=quest_id)

        elif (not choice3 == "None" and not choice3 == "") and (not choice2 == "None" and not choice2 == ""):
            db.execute("UPDATE questions SET choice2=:choice2, choice3=:choice3 WHERE id=:quest_id",\
            choice2=choice2, choice3=choice3, quest_id=quest_id)

        elif (not choice3 == "None" and not choice3 == "") and (choice2 == "None" or choice2 == ""):
            db.execute("UPDATE questions SET choice2=:choice3, choice3=NULL WHERE id=:quest_id",\
            choice3=choice3, quest_id=quest_id)
        else:
            db.execute("UPDATE questions SET choice2= NULL, choice3=NULL WHERE id=:quest_id",\
            quest_id=quest_id)

        db.execute("UPDATE questions SET question=:question, answer=:answer, choice1=:choice1, updatedAt=:updatedAt, type=:q_type WHERE id=:quest_id",\
        question=question, answer=answer, choice1=choice1, updatedAt=datetime.date.today(), q_type=q_type, quest_id=quest_id)

        return redirect("/memento")

@app.route("/deletememento", methods=["GET", "POST"])
@login_required
def delete_memento():
    """Delete Question"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        questID = request.form.get("questionID")
        db.execute("DELETE FROM questions WHERE id=:quest_id", quest_id=questID)

        return redirect("/memento")



@app.route("/remember", methods=["GET", "POST"])
@login_required
def remember():
    """Show all quizes created by user"""
    if request.method == "POST":
        selected_quiz = request.form.get("selected_quiz")

        questions = []
        answer_choice = []
        choices = []
        questiontype = []
        question_ids = []

        if selected_quiz == "random":
            rows = db.execute("SELECT * FROM questions WHERE user_id=:user_id", user_id=session["user_id"])
            random.shuffle(rows)
            for i in range(min(10, len(rows))):
                questions.append(rows[i]["question"])
                answer_choice.append(rows[i]["answer"])
                answer_choice.append(rows[i]["choice1"])
                if rows[i]["choice2"]:
                    answer_choice.append(rows[i]["choice2"])
                if rows[i]["choice3"]:
                    answer_choice.append(rows[i]["choice3"])
                choices.append(answer_choice[:])
                answer_choice.clear()
                questiontype.append(rows[i]["type"])

        else:
            quiz = (db.execute("SELECT * FROM quizes WHERE id=:quiz_id", quiz_id=selected_quiz))[0]
            question_ids = [int(i) for i in quiz["questions"].split(',')]
            rows = db.execute("SELECT * FROM questions WHERE id IN (:question_ids)", question_ids=question_ids)

            for row in rows:
                questions.append(row["question"])
                answer_choice.append(row["answer"])
                answer_choice.append(row["choice1"])
                if row["choice2"]:
                    answer_choice.append(row["choice2"])
                if row["choice3"]:
                    answer_choice.append(row["choice3"])
                choices.append(answer_choice[:])
                answer_choice.clear()
                questiontype.append(row["type"])

        shuffledChoices = []
        for choice in choices:
            shuffle=choice[:]
            random.shuffle(shuffle)
            shuffledChoices.append(shuffle[:])
            shuffle.clear()


        length = len(questions)

        return render_template("quiz.html", questions=questions, choices=choices, questiontype=questiontype, length=length, shuffledChoices=shuffledChoices, types=types)


    else:
        #Get quizes of the current user
        rows = db.execute("SELECT * FROM quizes WHERE user_id=:user_id", user_id=session["user_id"])
        questions = []
        questions_split = []
        quizes = []
        quiztype = []
        quizID = []
        create_date = []

        temp_quest_list = []

        for row in rows:
            quizes.append(row["quiz_name"])
            temp_quest_list = row["questions"].split(',')
            questions_split.append(temp_quest_list)
            questions.append(row["questions"])
            temp_quest_list.clear()
            quizID.append(row["id"])
            quiztype.append(row["quiz_type"])
            create_date.append(row["createdAt"])

        length = len(quizes)

        return render_template("remember.html", quizes=quizes, questions=questions, quiztype=quiztype, length=length, quizID=quizID, create_date=create_date)


@app.route("/deletequiz", methods=["GET", "POST"])
@login_required
def delete_quiz():
    """Delete Quiz"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        quizID = request.form.get("quizID")
        db.execute("DELETE FROM quizes WHERE id=:quiz_id", quiz_id=quizID)

        return redirect("/remember")


@app.route("/sharequiz", methods=["GET", "POST"])
@login_required
def share_quiz():
    """Share Quiz"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        quizID = request.form.get("quizID")
        db.execute("CREATE TABLE IF NOT EXISTS 'shared_quizes' ('id' INTEGER NOT NULL, 'user_id' INTEGER NOT NULL, 'quiz_id' INTEGER NOT NULL,\
                `sharedAt` DATETIME NOT NULL, PRIMARY KEY ('id'));")

        db.execute("INSERT INTO shared_quizes(user_id, quiz_id, sharedAt) VALUES(:user_id, :quiz_id, :sharedAt)",\
        user_id=session["user_id"], quiz_id=quizID, sharedAt=datetime.date.today())

        flash('Quiz is successfully shared!', 'success')
        # Redirect user to where s/he left
        return redirect("/remember")

@app.route("/test_yourself", methods=["GET", "POST"])
@login_required
def test_yourself():
    """Show all quizes shared publicly"""
    if request.method == "POST":
        selected_quiz = request.form.get("quizID")

        questions = []
        answer_choice = []
        choices = []
        questiontype = []
        question_ids = []

        quiz = (db.execute("SELECT * FROM quizes WHERE id=:quiz_id", quiz_id=selected_quiz))[0]
        question_ids = [int(i) for i in quiz["questions"].split(',')]
        rows = db.execute("SELECT * FROM questions WHERE id IN (:question_ids)", question_ids=question_ids)

        for row in rows:
            questions.append(row["question"])
            answer_choice.append(row["answer"])
            answer_choice.append(row["choice1"])
            if row["choice2"]:
                answer_choice.append(row["choice2"])
            if row["choice3"]:
                answer_choice.append(row["choice3"])
            choices.append(answer_choice[:])
            answer_choice.clear()
            questiontype.append(row["type"])

        shuffledChoices = []
        for choice in choices:
            shuffle=choice[:]
            random.shuffle(shuffle)
            shuffledChoices.append(shuffle[:])
            shuffle.clear()


        length = len(questions)

        return render_template("quiz.html", questions=questions, choices=choices, questiontype=questiontype, length=length, shuffledChoices=shuffledChoices, types=types)


    else:
        #Get quizes of the current user
        rows = db.execute("SELECT * FROM shared_quizes")
        shared_quiz_id = []
        user = []
        for row in rows:
            shared_quiz_id.append(row["quiz_id"])
            user.append(row["user_id"])

        shared_quiz_id = [int(i) for i in shared_quiz_id]

        questions = []
        questions_split = []
        quizes = []
        quiztype = []
        quizID = []
        create_date = []
        temp_quest_list = []

        rows2 = db.execute("SELECT * FROM quizes WHERE id IN (:shared_quiz_id)", shared_quiz_id=shared_quiz_id)

        for row in rows2:
            quizes.append(row["quiz_name"])
            temp_quest_list = row["questions"].split(',')
            questions_split.append(temp_quest_list)
            questions.append(row["questions"])
            temp_quest_list.clear()
            quizID.append(row["id"])
            quiztype.append(row["quiz_type"])
            create_date.append(row["createdAt"])

        length = len(quizes)

        return render_template("test_yourself.html", quizes=quizes, questions=questions, quiztype=quiztype, length=length, quizID=quizID, create_date=create_date)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["passwordHash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/about")
def about():
    """Show about page"""

    # Redirect user to login form
    return render_template("about.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register User """

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password", 403)

        # Ensure passwords that are submitted match
        elif not request.form.get("confirmation") == request.form.get("password"):
            return apology("Password does not match", 403)

        # Ensure firstname was submitted
        elif not request.form.get("firstname"):
            return apology("one must have a name", 403)

        # Ensure lastname was submitted
        elif not request.form.get("lastname"):
            return apology("one must have a last name", 403)

        # Ensure email was submitted
        elif not request.form.get("email"):
            return apology("must provide email address", 403)

        # Ensure phone was submitted
        elif not request.form.get("phone"):
            return apology("must provide phone number", 403)

        # Ensure agree-term box is checked
        elif not request.form.get("agree-term"):
            return apology("Terms and Conditions must be accepted", 403)

        elif not request.form.get("password").isalnum() or len(request.form.get("password")) < 6:
            return apology("Password must be consist of letters and numbers with at least 6 characters", 403)


        # Create tables if they doesnt exist
        db.execute("CREATE TABLE IF NOT EXISTS 'users' ('id' INTEGER NOT NULL, 'firstName' VARCHAR(50) NULL DEFAULT NULL, 'lastName' VARCHAR(50) NULL DEFAULT NULL,\
                    'mobile' VARCHAR(15) NULL UNIQUE, 'email' VARCHAR(50) NULL UNIQUE, 'passwordHash' VARCHAR(32) NOT NULL, 'host' TINYINT(1) NOT NULL DEFAULT 0,\
                    'registeredAt' DATETIME NOT NULL, 'lastLogin' DATETIME NULL DEFAULT NULL, 'intro' TINYTEXT NULL DEFAULT NULL, 'profile' TEXT NULL DEFAULT NULL, \
                    'username' VARCHAR(15) NOT NULL UNIQUE, PRIMARY KEY ('id'));")

        # Query database to check if username already exist
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) >= 1:
            return apology("Username already exists", 403)


        try:
            db.execute("INSERT INTO users(username, passwordHash, firstName, lastName, mobile, email, registeredAt) VALUES(:username, :hash, :firstname, :lastname, :mobile, :email, :datetime)",\
            username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")), firstname=request.form.get("firstname"), lastname=request.form.get("lastname"),\
            mobile=request.form.get("phone"), email=request.form.get("email"), datetime=datetime.date.today())

        except:
            return apology("Email or Mobile Phone already exist", 403)

        # Query database to check if registration is succesful
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists
        if len(rows) != 1:
            return apology("Registration is not successful", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash('Registered!', 'success')
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

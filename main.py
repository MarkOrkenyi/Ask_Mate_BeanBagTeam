from flask import Flask, render_template, request, redirect
import function
import datetime


app = Flask(__name__)

# Mark begins


@app.route("/question/<question_id>")
def question_details(question_id):
    questions_list = function.read_csv("./data/question.csv", True)
    for row in questions_list:
        if question_id == row[0]:
            question = row
            break
    print(questions_list)
    question_message = question[5]
    question_title = question[4]
    answers = []
    answers_list = function.read_csv("./data/answer.csv", False)
    for row in answers_list:
        if question_id == row[3]:
            answers.append(row)
    return render_template("question_details.html",
                           question_title=question_title,
                           question_message=question_message,
                           question=question,
                           answers=answers,
                           question_id=question_id)


@app.route("/question/<question_id>/new-answer", methods=['POST'])
def new_answer(question_id):
    return render_template("answer.html", question_id=question_id)


@app.route("/question/<question_id>/new-answer-submit", methods=['POST'])
def add_new_answer(question_id):
    to_add = []
    time = datetime.datetime.now()
    answer = str(request.form['newanswer'])
    to_add.append(function.get_new_id("./data/answer.csv", False))
    to_add.append(time)
    to_add.append(0)
    to_add.append(question_id)
    to_add.append(answer)
    function.write_csv("./data/answer.csv", to_add, False)
    return redirect("/question/{}".format(question_id))
# MARK ends


# OLLE begins


@app.route("/")
@app.route("/list")
def show_list():
    '''Render the Questiontable'''
    header_row = ["ID",
                  "Title",
                  "Message",
                  "Views",
                  "Votes",
                  "",
                  "Time",
                  ]
    question_table = function.read_csv("./data/question.csv", True)
    question_table = sorted(question_table, key=lambda time: time[1], reverse=True)
    return render_template('list.html', question_table=question_table, header_row=header_row)
# OLLE end

# Annamari begins


@app.route('/newquestion', methods=['GET', 'POST'])
def add_new_question():
    if request.method == 'GET':
        return render_template("question.html")

    elif request.method == 'POST':
        id_ = function.get_new_id('./data/question.csv', True)
        submisson_time = datetime.datetime.now()
        view_number = '0'
        vote_number = '0'
        title = request.form["title"]
        message = request.form["message"]
        fieldnames = [id_, submisson_time, view_number, vote_number, title, message]
        function.write_csv('./data/question.csv', fieldnames, True)
        return redirect("./")
# Annamari ends


if __name__ == '__main__':
    app.run(debug=True)

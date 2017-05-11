from flask import Flask, render_template, request, redirect
import function
import time


app = Flask(__name__)


@app.route("/")
@app.route("/list")
def show_list():
    '''Renders the Questions table'''
    header_row = ["ID",
                  "Title",
                  "Message",
                  "Views",
                  "Votes",
                  "",
                  "Time",
                  "Delete"
                  ]
    question_table = function.read_csv("./data/question.csv", "question")
    question_table = sorted(question_table, key=lambda time_: time_[1], reverse=True)
    return render_template('list.html', question_table=question_table, header_row=header_row)


@app.route("/question/<question_id>")
def question_details(question_id):
    '''Renders question_details.html with the details of a given question'''
    questions_list = function.read_csv("./data/question.csv", "question")
    for row in questions_list:
        if question_id == row[0]:
            question = row
            break
    question_message = question[5]
    question_title = question[4]
    answers = []
    answers_list = function.read_csv("./data/answer.csv", "answer")
    answers_list = sorted(answers_list, key=lambda id_: id_[0],)
    for row in answers_list:
        if question_id == row[3]:
            answers.append(row)
    to_add = []
    for row in questions_list:
        if row[0] == question_id:
            for element in row:
                to_add.append(element)
    for row in questions_list:
        if row[0] == to_add[0]:
            questions_list.pop(questions_list.index(row))
    views = int(to_add[2])
    views += 1
    to_add[2] = str(views)
    questions_list.append(to_add)
    function.write_csv('./data/question.csv', questions_list, "question")
    return render_template("question_details.html",
                           question_title=question_title,
                           question_message=question_message,
                           question=question,
                           answers=answers,
                           question_id=question_id)


@app.route('/newquestion', methods=['GET', 'POST'])
def add_new_question():
    '''Renders question.html to get a new question, then writes that out to the csv file
    \nRedirects to the questions list page'''
    if request.method == 'GET':
        return render_template("question.html")

    if request.method == "POST":
        id_ = function.get_new_id('./data/question.csv', "question")
        submisson_time = function.convert_time(time.time(), "decode")
        view_number = '0'
        vote_number = '0'
        title = request.form["title"]
        message = request.form["message"]
        new_row = [id_, submisson_time, view_number, vote_number, title, message]
        csv_data = function.read_csv("./data/question.csv", "question")
        csv_data.append(new_row)
        function.write_csv('./data/question.csv', csv_data, "question")
        return redirect("./")


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    '''Deletes a given question, then redirects to "./list"'''
    if request.method == 'POST':
        id_ = question_id
        delete_data = function.remove(function.read_csv('./data/question.csv', "question"), id_, 0)
        function.write_csv('./data/question.csv', delete_data, "question")
        answer_delete_data = function.remove(function.read_csv('./data/answer.csv', "answer"), id_, 3)
        function.write_csv('./data/answer.csv',  answer_delete_data, "answer")
        return redirect('./list')


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def new_answer(question_id):
    '''Renders answer.html to get a new answer, then writes that out to a csv file
    \nRedirects to the given question's detail page'''
    if request.method == 'GET':
        return render_template("answer.html", question_id=question_id)

    if request.method == 'POST':
        to_add = []
        answer = str(request.form['newanswer'])
        to_add.append(function.get_new_id("./data/answer.csv", "answer"))
        to_add.append(function.convert_time(time.time(), "decode"))
        to_add.append(0)
        to_add.append(question_id)
        to_add.append(answer)
        csv_data = function.read_csv("./data/answer.csv", "answer")
        csv_data.append(to_add)
        function.write_csv("./data/answer.csv", csv_data, "answer")
        return redirect("/question/{}".format(question_id))


@app.route("/question/<question_id>/edit", methods=['POST', 'GET'])
def edit_question(question_id):
    '''Renders question.html to edit a given question, then updates the question in the csv file
    \n Redirects to the question's detail page'''
    if request.method == 'GET':
        question_list = function.read_csv("./data/question.csv", "question")
        for row in question_list:
            if row[0] == question_id:
                question_title = row[4]
                question_message = row[5]
        return render_template("question.html", question_id=question_id, message=question_message, title=question_title)

    if request.method == 'POST':
        to_add = []
        message = request.form['message']
        title = request.form['title']
        data = function.read_csv("./data/question.csv", "question")
        for row in data:
            if row[0] == question_id:
                for element in row:
                    to_add.append(element)
        for row in data:
            if row[0] == to_add[0]:
                data.pop(data.index(row))
        to_add[4] = title
        to_add[5] = message
        data.append(to_add)
        function.write_csv('./data/question.csv', data, "question")
        return redirect("/question/{}".format(question_id))


@app.route('/question/<question_id>/vote-up', methods=['POST', 'GET'])
def question_vote_up(question_id):
    '''Increases the vote count of the given question'''
    to_add = []
    csv_data = function.read_csv('./data/question.csv', "question")
    for row in csv_data:
        if row[0] == question_id:
            for element in row:
                to_add.append(element)
    for row in csv_data:
        if row[0] == to_add[0]:
            csv_data.pop(csv_data.index(row))
    votes = int(to_add[3])
    votes += 1
    to_add[3] = str(votes)
    csv_data.append(to_add)
    function.write_csv('./data/question.csv', csv_data, "question")
    return redirect('./list')


@app.route('/question/<question_id>/vote-down', methods=['POST', 'GET'])
def question_vote_down(question_id):
    '''Decreases the vote count of the given question'''
    to_add = []
    csv_data = function.read_csv('./data/question.csv', "question")
    for row in csv_data:
        if row[0] == question_id:
            for element in row:
                to_add.append(element)
    for row in csv_data:
        if row[0] == to_add[0]:
            csv_data.pop(csv_data.index(row))
    votes = int(to_add[3])
    votes -= 1
    to_add[3] = str(votes)
    csv_data.append(to_add)
    function.write_csv('./data/question.csv', csv_data, "question")
    return redirect('./list')


@app.route('/answer/<answer_id>/vote-up', methods=['POST', 'GET'])
def answer_vote_up(answer_id):
    '''Increases the vote count of the given answer'''
    question_id = request.form['questionid']
    to_add = []
    csv_data = function.read_csv('./data/answer.csv', "answer")
    for row in csv_data:
        if row[0] == answer_id:
            for element in row:
                to_add.append(element)
    for row in csv_data:
        if row[0] == answer_id:
            csv_data.pop(csv_data.index(row))
    votes = int(to_add[2])
    votes += 1
    to_add[2] = str(votes)
    csv_data.append(to_add)
    function.write_csv('./data/answer.csv', csv_data, "answer")
    return redirect("./question/{}".format(question_id))


@app.route('/answer/<answer_id>/vote-down', methods=['POST', 'GET'])
def answer_vote_down(answer_id):
    '''Decreases the vote count of the given answer'''
    question_id = request.form['questionid']
    to_add = []
    csv_data = function.read_csv('./data/answer.csv', "answer")
    for row in csv_data:
        if row[0] == answer_id:
            for element in row:
                to_add.append(element)
    for row in csv_data:
        if row[0] == answer_id:
            csv_data.pop(csv_data.index(row))
    votes = int(to_add[2])
    votes -= 1
    to_add[2] = str(votes)
    csv_data.append(to_add)
    function.write_csv('./data/answer.csv', csv_data, "answer")
    return redirect("./question/{}".format(question_id))


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id):
    '''Deletes given answer, then redirects to the question's detail page'''
    question_id = request.form['questionid']
    answer_delete_data = function.remove(function.read_csv('./data/answer.csv', "answer"), answer_id, 0)
    function.write_csv('./data/answer.csv',  answer_delete_data, "answer")
    return redirect("/question/{}".format(question_id))


if __name__ == '__main__':
    app.run(debug=True)

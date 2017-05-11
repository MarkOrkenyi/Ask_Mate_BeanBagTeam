from flask import Flask
from flask import request
from flask import render_template
import function
import csv
from time import localtime, strftime
import base64
import datetime


app = Flask(__name__)


@app.route('/new_question', methods=['GET', 'POST'])
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


"""
@app.route('/new_question', methods=['GET', 'POST'])
def add_new_question():
    if request.method == 'GET':
        print('get')
        return render_template("question.html")

    elif request.method == 'POST':
        print('1ok')
        id_ = str(get_id(function.read_csv('./data/question.csv', True)))
        print(id_)
        submisson_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        print(submisson_time)
        view_number = '0'
        vote_number = '0'
        title = request.form["title"]
        print(title)
        message = request.form["message"]
        print(message)
        fieldnames = [id_, submisson_time, view_number, vote_number, title, message]
        function.write_csv('./data/question.csv', fieldnames, True)
        return render_template("question.html")


@app.route('/question/<question_id>/edit', methods=['POST', 'GET'])
def update_question(question_id=None):
    if request.method == 'GET':
        edit_data = function.read_csv('./data/question.csv', True)
        for line in edit_data:
            print(line)
            if line[0] == question_id:
                return render_template("question.html", title=line[4], message=line[5])

    elif request.method == 'POST':
        edit_title = request.form["title"]
        edit_message = request.form["message"]
        edit_data = function.read_csv('./data/question.csv', True)
        fieldnames = []
        for line in edit_data:
            if edit_data[0] == question_id:
                fieldnames.append(edit_data[0])
                fieldnames.append(edit_data[1])
                fieldnames.append(edit_data[2])
                fieldnames.append(edit_data[3])
        fieldnames.append(edit_title, edit_message)
        print(fieldnames)
        update_question = update(function.readcsv('./data/question.csv', True), id_, fieldnames)
        write_csv('/data/question.csv', update_question)
        return render_template("question.html", question_id=question_id)


def update(file_data, id_, field):
    for index, elements in enumerate(file_data):
        if elements[0] == id_:
            update_data = [n for n in field]
            file_data.pop(index)
            file_data.append(update_data)
    return file_data"""


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    if request.method == 'POST':
        id_ = question_id
        delete_data = question.remove(function.read_csv('./data/question.csv', True), id_, 0)
        encode_delete_data = question.encoder(delete_data, True)
        question.write_to_file('./data/question.csv', encode_delete_data)
# answer delete
        answer_delete_data = question.remove(function.read_csv('./data/answer.csv', False), id_, 3)
        answer_encode_delete_data = question.encoder(answer_delete_data, False)
        question.write_to_file('./data/answer.csv', answer_encode_delete_data)
        return redirect('./list')


def remove(file_data, id_, num):
    to_pop = []
    for index, elements in enumerate(file_data):
        if elements[num] == id_:
            to_pop.append(index)
    for i in reversed(list(map(int, to_pop))):
        file_data.pop(i)
    return file_data


def write_to_file(file_name, data):
    with open(file_name, "w") as file:
        for record in data:
            row = ','.join(record)
            file.write(row + "\n")


def encoder(content, question):
    for row in content:
        row[1] = row[1].strftime("%s")
        row[4] = bytes.decode(base64.b64encode(str.encode(row[4])))
        if question:
            row[5] = bytes.decode(base64.b64encode(str.encode(row[5])))
    return content


def main():
    app.run()


if __name__ == '__main__':
    main()

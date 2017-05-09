from flask import Flask
from flask import request
from flask import render_template
import function
import csv
from time import localtime, strftime

app = Flask(__name__)


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


def delete_question(question_id):
    id_ = request.form['delete_question']
    delete_data = remove(function.read_csv('./data/question.csv', True), id_)
    function.write_csv('./data/question.csv', delete_data, True)
    list_data = function.read_csv('./data/question.csv')
    return render_template("list.html", list_data=list_data)


def get_id(id_data):
    id_ = ['0']
    for data in id_data:
        id_.append(data[0])
    print(id_)
    max_id = max(map(int, id_))
    print(max_id)
    return (int(max_id) + 1)


def remove(file_data, id_):
    for index, elements in enumerate(file_data):
        if elements[0] == id_:
            file_data.pop(index)
            return file_data


def main():
    app.run()


if __name__ == '__main__':
    main()
